# Design System Strategy: Thermal Intelligence & Layered Depth

## 1. Overview & Creative North Star
**The Creative North Star: "The Thermal Sentinel"**

This design system is engineered to move away from the "SaaS-template" aesthetic into a realm of high-end, editorial precision. We are building a platform that monitors invisible threats; therefore, the UI must feel like a sophisticated instrument—authoritative, calm, and deeply layered. 

To break the traditional grid, we utilize **Intentional Asymmetry**. Larger display elements should push against the margins, while data density is managed through varying levels of "thermal" depth. We avoid the "flat" look of modern dashboards by treating the interface as a stack of semi-transparent, heat-sensitive lenses. The experience is not just seen; it is felt through tonal shifts and atmospheric gradients.

---

## 2. Colors: Tonal Atmosphere
The palette is built on a high-contrast foundation of deep obsidian and incandescent heat.

### The "No-Line" Rule
**Borders are a failure of hierarchy.** In this system, 1px solid borders are strictly prohibited for sectioning. Boundaries must be defined solely through background color shifts. Use `surface-container-low` sections against the `surface` background to create natural separation.

### Surface Hierarchy & Nesting
Depth is achieved through the physical stacking of containers:
- **Base Level:** `surface` (#0b0e14) — The infinite dark background.
- **Section Level:** `surface-container-low` (#10131a) — For large content blocks.
- **Component Level:** `surface-container` (#161a21) — For primary interactive cards.
- **Elevated Level:** `surface-container-highest` (#22262f) — For active states or floating modals.

### The Glass & Gradient Rule
To achieve a signature "premium" feel, floating elements (drawers, tooltips, navigation) must utilize **Glassmorphism**. 
- **Backdrop Blur:** 12px to 20px.
- **Fill:** `surface-variant` at 60% opacity.
- **Gradients:** Use a subtle linear gradient on primary CTAs transitioning from `primary` (#ff906d) to `primary-container` (#ff784d) at a 135° angle. This adds "soul" and prevents the orange from feeling "flat" or "cheap."

---

## 3. Typography: Editorial Authority
We use a dual-font strategy to balance character with readability.

*   **Display & Headlines:** `Plus Jakarta Sans`. This typeface provides the geometric precision required for a tech-forward platform. Use `display-lg` (3.5rem) with tight letter-spacing (-0.02em) for hero data points to create an "Editorial Impact."
*   **Body & UI:** `Inter`. The industry standard for legibility. Inter handles the heavy lifting of data-dense heatwave reports and granular risk metrics.

**Hierarchy as Identity:** 
Use extreme scale. Pair a `display-md` temperature reading with a `label-sm` unit of measurement. This contrast creates a sophisticated, "Swiss-style" information density that feels intentional and high-end.

---

## 4. Elevation & Depth: Tonal Layering

### The Layering Principle
Avoid drop shadows for standard cards. Instead, place a `surface-container-lowest` card on a `surface-container-low` section. This creates a "recessed" or "pressed" look that is more modern and cleaner than traditional shadows.

### Ambient Shadows
When a "floating" effect is mandatory (e.g., a critical alert modal):
- **Blur:** 40px - 60px.
- **Opacity:** 6% - 8%.
- **Color:** Use `surface-tint` (#ff906d) instead of black. A tinted shadow mimics the way heat glows in the dark, creating a more cohesive atmospheric experience.

### The "Ghost Border" Fallback
If a border is required for accessibility, use the **Ghost Border**: `outline-variant` (#45484f) at 15% opacity. Never use 100% opaque lines.

---

## 5. Components: Precision Instruments

### Cards & Lists
*   **Style:** Forbid the use of divider lines.
*   **Execution:** Use `md` (0.75rem) or `lg` (1rem) vertical white space to separate list items. Use a subtle background hover state (`surface-bright`) to indicate interactivity.
*   **Radius:** Always use `lg` (1rem) for primary cards and `xl` (1.5rem) for main dashboard containers.

### Buttons
*   **Primary:** Gradient fill (`primary` to `primary-container`). `full` roundedness. No border.
*   **Secondary:** Ghost style. Transparent fill with a `Ghost Border`. Text color `primary`.
*   **States:** On hover, primary buttons should increase in "glow" (increase shadow spread of the tinted ambient shadow), not just change color.

### Risk Indicators (Chips)
Instead of standard badges, use **Micro-Gradients**:
- **High Risk:** `error` to `error_dim` gradient.
- **Medium Risk:** `secondary` to `secondary_dim` gradient.
- **Low Risk:** `tertiary` to `tertiary_dim` gradient.
These should be small, pill-shaped (`full` radius), and use `on-primary-fixed` black text for maximum legibility against the vibrant heat colors.

### Input Fields
*   **Surface:** `surface-container-lowest`.
*   **Focus State:** Shift background to `surface-container-high` and apply a 1px "Ghost Border" of `primary`. Do not use heavy focus rings.

---

## 6. Do’s and Don’ts

### Do
*   **Do** use asymmetrical layouts. Let a chart bleed off the right side of a card to suggest continuity.
*   **Do** use "Breathing Room." High-end design is defined by what you leave out. Increase your margins by 20% more than you think is necessary.
*   **Do** use subtle motion. Background gradients should have a very slow (30s) "pulse" to mimic the shimmering of heat.

### Don’t
*   **Don't** use pure white (#FFFFFF) for text. Use `on-surface` (#e4e5ee) to reduce eye strain in dark mode.
*   **Don't** use icons as purely decorative elements. Every icon must serve a functional purpose in the data hierarchy.
*   **Don't** use standard 1px dividers. If you feel the need to "separate," use a 12px gap of empty space or a subtle shift from `surface-container-low` to `surface-container-lowest`.