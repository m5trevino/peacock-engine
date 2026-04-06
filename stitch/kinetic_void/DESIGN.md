# Design System Specification

## 1. Overview & Creative North Star: "The Kinetic Observatory"
The design system is a high-performance framework engineered for deep-data immersion. It moves away from the sterile, flat aesthetic of common SaaS platforms toward a "Kinetic Observatory" philosophy. This North Star prioritizes atmospheric depth, high-speed visual processing, and high-tech elegance. 

By utilizing an obsidian teal base (`#0c0e17`) and hyper-vibrant cyan (`#00e3fd`) and magenta (`#ff009d`) accents, we create a sensory experience that feels both authoritative and electric. The system breaks the "template" look through intentional asymmetry in layout, overlapping data visualizations, and an editorial typography scale that commands attention.

## 2. Colors & Surface Philosophy
The palette is a study in tonal contrast, designed to minimize eye strain while maximizing the "pop" of critical data points.

### The "No-Line" Rule
To achieve a premium, high-tech finish, **1px solid borders are prohibited for sectioning.** Boundaries must be defined exclusively through background color shifts or tonal transitions.
- Use `surface-container-low` (`#11131d`) for secondary sidebars or backgrounds.
- Place `surface-container` (`#171924`) or `surface-container-high` (`#1c1f2b`) on top to create logical containment without the visual clutter of lines.

### Surface Hierarchy & Nesting
Treat the UI as physical layers of Obsidian and Frosted Glass. 
*   **Base:** `background` (#0c0e17).
*   **Layer 1 (The Canvas):** `surface-container-low`.
*   **Layer 2 (The Cards):** `surface-container-high`.
*   **Layer 3 (The Interactives):** `surface-bright`.

### The "Glass & Gradient" Rule
For floating elements or hero modules, use **Glassmorphism**: 
- Background: `surface-variant` (`#222532`) at 60% opacity.
- Backdrop Blur: `20px` to `40px`.
- **Signature Textures:** Incorporate linear gradients from `primary` (#82ecff) to `primary-container` (#01e3fd) for active states and critical CTAs to inject "soul" into the data-heavy environment.

## 3. Typography: Editorial Precision
The system pairs the industrial, high-contrast **Space Grotesk** with the clean, humanistic **Manrope**.

*   **The Display Scale:** Use `display-lg` (3.5rem) and `display-md` (2.75rem) in Space Grotesk for high-impact numbers and dashboard headers. These should be high-contrast (`on-surface`).
*   **The Narrative Scale:** `headline-sm` (1.5rem) sets the stage for data modules, while `body-lg` (Manrope, 1rem) ensures long-form data notes remain legible.
*   **Hierarchy through Tonality:** Use `on-surface-variant` (`#aaaab7`) for secondary labels (`label-md`) to ensure the primary headlines remain the focal point.

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are largely replaced by **Tonal Layering** to maintain a clean, high-tech aesthetic.

*   **The Layering Principle:** Depth is achieved by stacking. A `surface-container-lowest` card placed on a `surface-container-low` section creates a natural "recessed" look.
*   **Ambient Shadows:** When an element must float (e.g., a modal or dropdown), use a shadow tinted with the `primary` hue:
    *   `box-shadow: 0 20px 40px rgba(0, 227, 253, 0.08);`
*   **The "Ghost Border" Fallback:** If containment is strictly required for accessibility, use a **Ghost Border**: `outline-variant` (`#464752`) at 15% opacity. Never use 100% opaque outlines.

## 5. Components

### Buttons
- **Primary:** A vibrant gradient of `primary` to `primary-dim`. Use `on-primary` for text. Roundedness: `full` or `xl`.
- **Secondary:** Transparent background with a `Ghost Border` and `primary` text.
- **Tertiary:** Text-only using `tertiary` (#ff9e6d) for high-alert actions or warnings.

### Cards & Data Modules
- **Constraint:** Forbid divider lines within cards. 
- **Separation:** Use `8px` to `16px` of vertical white space or a subtle background shift to `surface-container-highest` for internal card sectioning.
- **Header:** Always lead with a `title-sm` or `label-md` in `on-surface-variant`.

### Input Fields
- **Surface:** Use `surface-container-highest`. 
- **Active State:** A `primary` bottom-glow (2px glow) rather than a full bounding box.
- **Typography:** Placeholder text should use `label-md` in `outline`.

### High-Tech Accents (Bespoke)
- **Data Pills:** Use `secondary_container` (#b7006f) with `on_secondary_container` text for ROI or growth metrics.
- **Glow Indicators:** For status lights (Online/Active), use a `primary` or `tertiary` dot with a 4px blur-radius glow of the same color.

## 6. Do's and Don'ts

### Do
- **Do** use `primary` and `secondary` colors for data visualization bars with subtle 3D-esque gradients.
- **Do** leverage asymmetric padding (e.g., more padding on the left of a container than the top) to create a modern editorial feel.
- **Do** use `9999px` (full) roundedness for selection chips to contrast with the `xl` (1.5rem) roundedness of large containers.

### Don't
- **Don't** use pure black `#000000` for backgrounds unless it is for `surface-container-lowest` in a deeply nested module.
- **Don't** use 1px solid white or grey lines to separate content; it breaks the "Kinetic Observatory" immersion.
- **Don't** use standard "Material" blue. Stick strictly to the Cyan/Magenta/Obsidian teal tokens to maintain the signature brand identity.
- **Don't** overcrowd the viewport. If a dashboard feels "busy," increase the usage of `surface-dim` to create breathing room between data clusters.