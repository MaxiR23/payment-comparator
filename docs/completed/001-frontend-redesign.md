# 001 — Frontend redesign — completado

## Resumen

Rediseño completo del frontend con estética financiera moderna: Swiss grid, layout tipo ledger, tipografía IBM Plex.

## Dirección implementada

Base Dirección B (Swiss grid / contabilidad de precisión) con elementos de Dirección A:
- IBM Plex Mono para todos los datos y números (con `font-variant-numeric: tabular-nums`)
- Números de sección grandes y ligeros (`01`, `02`, `03`) en color `var(--rule)` como anclas estructurales
- Separadores hairline (`1px solid var(--rule)`) entre secciones en lugar de cards
- Fondo `#FAF8F5` (blanco cálido en lugar de blanco puro)

Paleta final:
- `--bg: #FAF8F5` — fondo cálido
- `--ink: #0B1628` — texto principal y botón CTA
- `--red: #B91C1C` — diferencias / alertas
- `--green: #166534` — total / éxito
- `--rule: #DDD8D0` — hairlines y section nums
- `--muted: #6B6560` — labels y hints

## Archivos modificados

- `templates/index.html` — nueva estructura: `<section class="form-section">` con `.section-label`, `.drop-meta`, `.ledger` rows; sin emojis; sin inline onclick
- `static/css/style.css` — rewrite completo; IBM Plex Sans + IBM Plex Mono desde Google Fonts; sin border-radius; sin sombras; sin cards

## Decisiones técnicas

- Se eliminó `.icon` (tenía emojis). No rompió nada: los JS files (`ui.js`, `files.js`) nunca referencian `.icon`.
- Se eliminó `onclick="clearAll()"` inline de `btn-clear` — es redundante porque `main.js` ya registra el listener vía `addEventListener`. Ambos apuntan al mismo handler.
- La clase dual `btn-run btn-clear` del original se separó en `btn-run` y `btn-clear` independientes — el JS solo referencia por ID, no por clase.
- Se cambió `.metric.warn/.ok` → `.ledger-row.warn/.ok` con valores alineados a la derecha. Los IDs `v-dif`, `v-falt`, `v-total` (que usa `ui.js`) se preservaron intactos.
- La sección 03 (Resultado) vive dentro de `#results`, que el JS controla con `style.display = 'block'/'none'` — comportamiento idéntico al original.