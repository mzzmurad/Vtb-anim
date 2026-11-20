VTB cake logo: scene files for Cinema 4D
=========================================

One whole cake, a knife makes four cuts, two strips slide out and the three VTB bars remain;
the camera follows the knife in close-up, then orbits up to the level logo.
30 fps, frames 0-269 (9 s), 1080 x 1920 (9:16).

Files
-----
vtb-cake-logo_stepped.fbx   <- START HERE. Camera, models, lights, materials and all animation.
                               Stepped timing: poses change 12 times a second, like the video.
vtb-cake-logo_smooth.fbx    Same scene, but the motion moves on every frame (no stepping).
vtb-cake-logo_stepped.abc   Alembic version (camera + models + animation, no materials).
vtb-cake-logo_stepped.blend Blender version (camera lens and depth-of-field focus keyed).
vtb-cake-logo_*.glb         glTF versions (universal backup).
vtb-cake-logo_*.camera.json Per-frame camera vertical field of view and focus distance.

Opening in Cinema 4D
--------------------
1. Edit > Project Settings: set FPS to 30 before importing.
2. File > Open (or Merge) vtb-cake-logo_stepped.fbx. In the FBX import options, turn on
   Cameras, Lights, Materials, Textures (embedded) and Animation / Tracks.
3. Set the render output to 1080 x 1920, frames 0 to 269, and look through the "Camera" object.

How the animation is built
--------------------------
- Camera: position, rotation and focal length are keyed on every frame. Film gate: 36 mm horizontal.
- Knife, the two cut strips ("Piece_stripA", "Piece_stripB"), the cut lines ("Cut_line_1..4") and
  the candle flames are keyed on every frame.
- The cake swaps between bodies as it is cut. These switch on and off with stepped scale keys (0 = hidden):
  "Body_whole_cake" until the first strip is cut, then "Body_lower_after_cut_1_2", then the final
  pieces "Body_bar1/2/3" (plus the strip bodies). If you replace a body, keep it under the same object.
- Units: 1 scene unit = 1 m, so the cake is about 8.2 m wide. Scale on import if you prefer.

Not in the files (these were effects in the video, rebuild them in C4D)
------------------------------------------------------------------------
- Fur / plush look: add Hair or Fur to the icing, sponge, cream layers and piped rosettes
  (short, dense, slightly combed; darker roots).
- Depth of field: the focus distance per frame is in the .camera.json file (and keyed in the .blend).
  Aim the camera's focus at the knife in the close-ups, and use only a little blur in the end shot.
- Glow on the flames: the flame materials are emissive; add Glow / bloom in your renderer.
- Background: a vertical gradient from #0755C2 (top) to #67C6FF (bottom).
- Shadows: the "Floor" object stands in for the shadow-only floor; give it a Shadow Catcher /
  Compositing tag (background compositing) so only the shadows show.
- Look: stepped timing (12 poses a second, held for 2-3 frames) and no motion blur.
