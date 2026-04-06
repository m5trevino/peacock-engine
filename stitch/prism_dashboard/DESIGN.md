# Design System Specification: Premium Analytics

## 1. Overview & Creative North Star

### The Creative North Star: "The Kinetic Observatory"
This design system is engineered to transform static data into a living, breathing digital environment. Moving away from the "flat box" aesthetic of standard SaaS dashboards, "The Kinetic Observatory" treats the interface as a high-fidelity lens. It utilizes deep, multi-dimensional space, glassmorphic clarity, and vibrant energy conduits to guide the user’s eye through complex information.

**Breaking the Template:**
To achieve a bespoke, high-end editorial feel, designers must embrace **intentional asymmetry**. Layouts should not be rigid 12-column grids; instead, use overlapping components and varying card heights to create a sense of organic growth. Typography scale is pushed to extremes—pairing massive, technical display headers with tiny, hyper-legible labels—to establish an authoritative hierarchy that feels curated rather than generated.

---

## 2. Colors & Surface Logic

The palette is rooted in a "Midnight-Plus" philosophy: deep blacks and purples form the void, while neon accents act as light sources within the interface.

### The "No-Line" Rule
**Explicit Instruction:** Prohibit the use of 1px solid borders for sectioning. Structural boundaries must be defined solely through background color shifts or tonal transitions.
- Use `surface-container-low` (#11131d) for secondary sections sitting atop the base `background` (#0c0e17).
- Use `surface-bright` (#282b3a) for highlighted interactive zones.

### Surface Hierarchy & Nesting
Treat the UI as physical layers of frosted material.
1.  **Base Layer:** `surface` (#0c0e17) — The infinite canvas.
2.  **Middle Layer:** `surface-container` (#171924) — Standard content containers.
3.  **Top Layer:** `surface-container-highest` (#222532) — Floating panels or active states.

### The "Glass & Gradient" Rule
Floating elements (Modals, Hover Tooltips, Popovers) must use **Glassmorphism**.
- **Background:** `surface-variant` (#222532) at 60% opacity.
- **Effect:** 20px - 40px Backdrop Blur.
- **Visual Soul:** Apply a linear gradient (Primary #b6a0ff to Primary-Dim #7e51ff) at 15% opacity as an overlay to main CTAs to prevent "flatness."

---

## 3. Typography

The typography strategy leverages two distinct personalities: the technical precision of **Space Grotesk** and the modern utility of **Inter**.

| Level | Token | Font Family | Size | Character |
| :--- | :--- | :--- | :--- | :--- |
| **Display** | display-lg | Space Grotesk | 3.5rem | Bold, technical, impactful. |
| **Headline**| headline-md | Space Grotesk | 1.75rem | Clear, editorial structure. |
| **Title** | title-md | Inter | 1.125rem | Sophisticated content headers. |
| **Body** | body-md | Inter | 0.875rem | High readability, neutral. |
| **Label** | label-sm | Inter | 0.6875rem | All-caps, tracked out for data. |

**Identity Logic:** Use `display` tokens for data points that need to "scream" importance. Use `label` tokens for technical metadata to give the dashboard a "cockpit" or "command center" feel.

---

## 4. Elevation & Depth

### The Layering Principle
Depth is achieved through **Tonal Layering**. Place a `surface-container-lowest` (#000000) card inside a `surface-container-low` (#11131d) section to create a recessed, "etched" look. Conversely, stack `surface-container-high` on the base background for a "lifted" feel.

### Ambient Shadows
Forget traditional drop shadows. Use **Ambient Glows**:
- **Color:** Use a tinted version of `primary` (#b6a0ff) or `secondary` (#00e3fd).
- **Settings:** 0px 10px 40px, 6% opacity. This mimics light refracting through the glass panels rather than a dark shadow on a wall.

### The "Ghost Border" Fallback
If accessibility requires a container edge, use a **Ghost Border**:
- **Token:** `outline-variant` (#464752) at 20% opacity.
- **Never** use 100% opaque borders; they shatter the glass illusion.

---

## 5. Components

### Buttons & Kinetic States
- **Primary:** Gradient from `primary` to `primary-container`. Soft inner glow (1px white at 10% opacity) on the top edge.
- **Secondary:** Transparent background with a `Ghost Border`.
- **Interaction:** On hover, buttons should "breathe"—a subtle scale (1.02x) and an increase in the ambient glow intensity.

### Data Chips
- **Selection:** Use `secondary` (#00e3fd) with `on-secondary` (#004d57) text.
- **Visual Style:** Pill-shaped (`rounded-full`), no border, high contrast.

### Input Fields
- **Base State:** `surface-container-highest` background.
- **Active State:** 1px `Ghost Border` becomes 100% `primary` opacity. Add a subtle 4px blur glow around the perimeter.
- **Error:** Use `error` (#ff6e84) for text and a `surface-container` background with an `error_container` subtle inner shadow.

### Cards & Lists
- **The Divider Ban:** Strictly forbid 1px lines between list items. Use **Vertical White Space** (16px - 24px) or alternating subtle background shifts (`surface-container` vs `surface-container-low`) to separate rows.

---

## 6. Do’s and Don’ts

### Do:
- **Do** use `tertiary` (Finor Yellow #ffe483) sparingly as a "high-alert" or "success-plus" accent to draw immediate attention to critical data.
- **Do** lean into `rounded-lg` (1rem) and `rounded-xl` (1.5rem) for main panels to soften the technical edge.
- **Do** use asymmetric spacing to group related data points, creating an editorial "story" on the page.

### Don’t:
- **Don't** use pure grey or white for text. Use `on-surface` (#f0f0fd) or `on-surface-variant` (#aaaab7) to maintain the dark-mode atmosphere.
- **Don't** allow cards to have hard corners. Every element should feel polished and ergonomic.
- **Don't** use standard "Box Shadows." If a card isn't clearly separated by its background tone, rethink the layering rather than adding a heavy shadow.