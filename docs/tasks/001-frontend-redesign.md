# 001 — Frontend redesign

## Goal
Redesign the frontend with a distinctive, professional aesthetic. The current design is generic dark-mode SaaS and lacks personality.

## Scope
Edit only:
- `templates/index.html`
- `static/css/style.css`
- `static/js/main.js` (only if necessary to preserve behavior)

Do NOT touch any Python files, routes, business logic, or configuration.

## Hard constraints
- All endpoints and POST/GET behavior stay identical.
- All existing JS interactions keep working (drag/drop, file labels, enable/disable logic, status states, results reveal, download flow).
- No emojis anywhere in code.
- Tabular figures for all numeric output.
- Light theme.
- No new dependencies (no Tailwind, no frameworks). Vanilla HTML/CSS/JS only.

## Process
1. Use the `frontend-design` skill first.
2. Before writing any code, propose 1–2 design directions with palette, typography, and a one-line concept. Wait for confirmation.
3. After my approval, implement.

## Reference direction (optional, "Comprobante")
- Warm off-white bg, deep ink text.
- Duotone signal system: vermilion `#C73E1D` for differences, deep green `#1B4332` for matches.
- Humanist sans for UI + monospace for numbers/codes (e.g., IBM Plex pair).
- Editorial layout: hairline rules between sections instead of card chrome; oversized monospace section numbers as structural anchors.
- Avoid: Inter everywhere, Tailwind purple/amber clichés, generic gray SaaS cards.

You may propose something different if you can justify it.

## Out of scope
- Do not change the comparison logic, file formats, or any endpoint.
- Do not "improve" copy. Keep Spanish labels intact (`Comparar archivos`, `Limpiar todo`, etc.).
- Do not modify `CLAUDE.md`, `requirements.txt`, or any non-frontend file.

## Definition of done
- Updated CSS, HTML, and (if needed) JS reflecting the agreed direction.
- Behavior verified intact.
- Summary at `docs/completed/001-frontend-redesign.md`.