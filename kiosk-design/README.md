# VTB queue kiosk home screen (direction H)

`vtb-kiosk-home-H.svg` is the 1200×800 home screen built for Figma: drag it onto a Figma canvas, or use File › Import.
Every element comes in as its own named layer:

- **Background**: Gradient (#0250BF → #1E7BE0 → #67C6FF), Logo mark (background) › Bar 1–3
- **Header**: Logo (mark + "VTB"), Language switch (AZ active, EN, RU), Time, Divider
- **Greeting**: Title, Subtitle (live text)
- **Service cards**: one group per card › Card background (drop shadow), Icon tile, Icon, Label, Chevron
- **Footer**: Button - Onlayn növbə, Button - Ana səhifə (disabled)

Text is set in Inter. Swap in VTB Group in Figma if it is installed.
`assets/` holds the logo mark (#00AEEF, exact geometry) and each icon as a separate SVG.
The slow bar motion on the published canvas isn't in the SVG. Recreate it in Figma with Smart Animate or in After Effects.

# Queue wait screen (direction H)

`vtb-queue-wait-H.svg` is the 1200×800 wait screen, also built for Figma import. Its layers: Background (gradient + logo mark bars), Header (logo, time), Promo slot (a 440×632 placeholder: drop your promo image in), and Queue board (title, column headers, one group per row with Row background, Ticket, Arrow and Desk). The top row is the "now calling" state: a white card with navy text. Waiting rows are translucent white.

# Home screen, navy version

`vtb-kiosk-home-navy.svg` is the 2000×1250 navy home screen (white header, navy body, diagonal stripe pattern), built for Figma import. Its layers: Background (navy fill, Stripe pattern › Stripe 1–16), Header (header background, logo, language switch, time), Greeting, Service cards (Card background, Icon tile, Icon, Label, Chevron), and Footer buttons.
Text is set as "VTB Group" with an Inter fallback, so it switches automatically where VTB Group is installed. The stripes are white at 28% opacity, tapering from 34 px to 3 px.
