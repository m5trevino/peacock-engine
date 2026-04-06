# Design System Document: High-End Trading Terminal

## 1. Overview & Creative North Star
**Creative North Star: The Celestial Observer**

This design system is not a dashboard; it is a high-precision instrument. Inspired by deep-space observation tools and elite financial terminals, it moves away from "flat" web conventions toward a multi-layered, atmospheric environment. 

The aesthetic is characterized by **"Technological Depth"**—an intentional departure from traditional grids through the use of glassmorphism, glowing data nodes, and an obsidian-base palette. We break the template look by prioritizing editorial-style spacing and subtle, high-contrast typography that emphasizes data as the hero. The goal is to make the user feel like they are piloting a sophisticated craft through a sea of information.

---

## 2. Colors
The palette is rooted in a dark, monochromatic obsidian base, punctuated by "Stellar Blue" to guide the eye toward critical actions and live data.

### The Palette (Material 3 Foundations)
*   **Background / Surface:** `#121318` (Surface) to `#0d0e13` (Surface Container Lowest).
*   **Primary Accent:** `#abc7ff` (Primary) with a focus on `#4d94ff` (Primary Container) for active states.
*   **Data Highlights:** `#ffb875` (Tertiary) for secondary metrics and `#ffb4ab` (Error) for market dips.
*   **Neutral Scales:** High-fidelity whites (`#ffffff`) for readability and `#c1c6d5` (On Surface Variant) for de-emphasized metadata.

### Styling Rules
*   **The "No-Line" Rule:** 1px solid borders are strictly prohibited for defining layout sections. Boundaries must be defined through **Background Shifting**. For example, a "Trading Module" should be set as `surface-container-low` against a `surface` background.
*   **Surface Hierarchy & Nesting:** Use the `surface-container` tiers to create a physical stack.
    *   *Base:* `surface`
    *   *Panels:* `surface-container-low`
    *   *Interactive Cards:* `surface-container-high`
*   **The "Glass & Gradient" Rule:** Primary CTAs and Floating Modals should utilize a `linear-gradient(135deg, #4d94ff 0%, #005cba 100%)`. Floating elements must use `backdrop-filter: blur(12px)` and a 20% opacity fill of the surface color to create the "frosted glass" terminal effect.
*   **Signature Textures:** Incorporate a subtle "Scanline" or "Noise" texture (opacity 2%) over the background to give the obsidian surfaces a tactile, hardware-terminal feel.

---

## 3. Typography
We utilize a technical sans-serif (Inter) to maintain a balance between elite editorial feel and mathematical precision.

*   **Display (L/M/S):** Large, airy, and high-contrast. Used for primary balance totals and total portfolio value.
*   **Headline & Title:** Used for module headers. These should be set with slightly wider letter-spacing (`0.02em`) to enhance the "technical" look.
*   **Body (L/M/S):** Optimized for high-density data reading. Use `body-md` for standard labels.
*   **Label (M/S):** Reserved for technical metadata (e.g., Timestamp, API status, Serial numbers).

**Editorial Intent:** Mix font weights intentionally. Pair a `headline-sm` (Medium weight) with a `label-md` (Regular weight, 60% opacity) to create an information hierarchy that feels curated rather than crowded.

---

## 4. Elevation & Depth
In this system, depth is a function of light and translucency, not shadow.

*   **The Layering Principle:** Avoid drop shadows on nested items. If a card sits inside a panel, the card should simply be one step higher on the `surface-container` scale.
*   **Ambient Shadows:** For floating elements (Modals, Hover Tooltips), use a "Celestial Glow" shadow: `box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 15px rgba(77, 148, 255, 0.05)`. This adds a subtle blue tint to the shadow, mimicking the glow of the screen.
*   **The "Ghost Border" Fallback:** Where separation is mission-critical (e.g., input fields), use a "Ghost Border": `1px solid rgba(139, 145, 158, 0.15)`. It should be barely perceptible.
*   **Glassmorphism:** Apply to any element that overlays data. Use `outline-variant` at 10% opacity for the "edge" of the glass to catch the light.

---

## 5. Components

### Buttons
*   **Primary:** Solid `primary-container` gradient. High-contrast `on-primary-fixed` text. Roundedness: `md` (0.375rem).
*   **Secondary/Ghost:** `outline` border at 20% opacity. Text in `primary`. On hover, the background fills to 10% opacity.

### Chips (Time Toggles/Filters)
*   Styled as "Pill" shapes (`full` roundedness). Active state uses `surface-bright` with a `primary` subtle glow. Inactive states should have no background, only `on-surface-variant` text.

### Input Fields
*   Background: `surface-container-highest`.
*   Border: Bottom-only "Ghost Border" for a sleek, terminal-like entry. 
*   Focus State: The bottom border transitions to `stellar-blue` with a 4px soft outer glow.

### Charts & Graphs
*   **The "Pulse" Line:** Lines should have a `2px` stroke with a `box-shadow` (glow) of the same color.
*   **Data Points:** Use `signal-white` for active hover points to create high-contrast focus.
*   **Fills:** Use a vertical gradient fill from `primary` (20% opacity) at the top to transparent at the bottom of the chart area.

### Cards & Lists
*   **Constraint:** No divider lines.
*   **Spacing:** Use `1.5rem` (24px) vertical padding to separate list items. Use a `surface-container-low` hover state to indicate interactivity.

---

## 6. Do's and Don'ts

### Do:
*   **Do** use asymmetrical layouts. A sidebar that doesn't reach the bottom or a floating header adds to the "Terminal" feel.
*   **Do** use `letter-spacing` on labels to give a "machine-read" aesthetic.
*   **Do** lean into the "Stellar Blue" glow for success states and interactive "hotspots."

### Don't:
*   **Don't** use pure black (`#000000`). It kills the depth. Always use the Obsidian base (`#121318`).
*   **Don't** use standard 1px borders. If you feel you need a line, use a background color change instead.
*   **Don't** use heavy shadows. They feel "Web 2.0." Stick to tonal layering and glassmorphism.
*   **Don't** crowd the data. High-end systems feel premium because they "waste" space to provide clarity.