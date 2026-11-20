"""Turn the baked glTF files from cake/export.mjs into Cinema 4D-friendly files.

    python-with-bpy cake/c4d_export.py out/cinema4d

For each vtb-cake-logo_<mode>.glb it writes vtb-cake-logo_<mode>.fbx (camera with animated focal length,
animated knife / strips / cut lines / flames, pieces switching on and off as scale 0/1, lights, materials
and embedded textures). For the stepped version it also writes an Alembic (.abc) and a .blend.
"""
import json
import math
import os
import sys

import bpy

out = os.path.abspath(sys.argv[-1])


def all_fcurves():
    """F-curves of every action (Blender 4.4+ keeps them in layered actions: layers → strips → channelbags)."""
    for a in bpy.data.actions:
        if hasattr(a, "layers"):
            for layer in a.layers:
                for strip in layer.strips:
                    for cb in getattr(strip, "channelbags", []):
                        yield from cb.fcurves
        else:
            yield from a.fcurves

for mode in ("stepped", "smooth"):
    glb = os.path.join(out, f"vtb-cake-logo_{mode}.glb")
    if not os.path.exists(glb):
        continue
    meta = json.load(open(os.path.join(out, f"vtb-cake-logo_{mode}.camera.json")))
    fps, frames = meta["fps"], meta["frames"]

    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = fps
    sc.frame_start, sc.frame_end = 0, frames - 1
    sc.render.resolution_x, sc.render.resolution_y = meta["width"], meta["height"]

    bpy.ops.import_scene.gltf(filepath=glb)

    # the glTF importer may place keys from frame 0 or 1: line the first key up with frame 0
    first = min((fc.keyframe_points[0].co.x for fc in all_fcurves() if fc.keyframe_points), default=0)

    cam = next(o for o in sc.objects if o.type == "CAMERA")
    cam.name = "Camera"
    sc.camera = cam
    # 36 mm horizontal film gate (Cinema 4D's default), lens from the horizontal angle of view
    cam.data.sensor_fit = "HORIZONTAL"
    cam.data.sensor_width = 36.0
    cam.data.sensor_height = 36.0 * meta["height"] / meta["width"]   # film aspect = frame aspect (9:16)
    cam.data.clip_start, cam.data.clip_end = 0.05, 200.0
    aspect = meta["width"] / meta["height"]
    for f, fov in enumerate(meta["fov_vertical_deg"]):
        hfov = 2 * math.atan(math.tan(math.radians(fov) / 2) * aspect)
        cam.data.lens = 18.0 / math.tan(hfov / 2)
        cam.data.keyframe_insert("lens", frame=f + first)
    cam.data.dof.use_dof = True                      # depth of field: focus on the knife's focus point, as in the film
    cam.data.dof.aperture_fstop = 2.8
    for f, d in enumerate(meta.get("focus_distance", [])):
        cam.data.dof.focus_distance = d
        cam.data.dof.keyframe_insert("focus_distance", frame=f + first)

    if first != 0:
        for fc in all_fcurves():
            for k in fc.keyframe_points:
                k.co.x -= first; k.handle_left.x -= first; k.handle_right.x -= first
            fc.update()
    print(f"{mode}: first key was at frame {first}, now 0")
    sc.frame_set(0)

    fbx = os.path.join(out, f"vtb-cake-logo_{mode}.fbx")
    bpy.ops.export_scene.fbx(
        filepath=fbx, use_selection=False, object_types={"CAMERA", "EMPTY", "LIGHT", "MESH"},
        apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y",
        bake_anim=True, bake_anim_use_all_bones=False, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=False,
        bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=0.0,
        path_mode="COPY", embed_textures=True, add_leaf_bones=False,
    )
    print("wrote", fbx)

    if mode == "stepped":
        abc = os.path.join(out, "vtb-cake-logo_stepped.abc")
        bpy.ops.wm.alembic_export(filepath=abc, start=0, end=frames - 1, selected=False,
                                  flatten=False, uvs=True, normals=True, vcolors=True, as_background_job=False)
        print("wrote", abc)
        blend = os.path.join(out, "vtb-cake-logo_stepped.blend")
        bpy.context.preferences.filepaths.save_version = 0   # no .blend1 backup
        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
        print("wrote", blend)
