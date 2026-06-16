// INFO: maneja la selección de archivos y la lógica de arrastrar y soltar (drag & drop)
import { state } from './state.js';
import { updateFileUI, updateButtons } from './ui.js';

/**
 * maneja la selección de archivos desde el input
 * @param {string} key
 * @param {HTMLInputElement} input
 */
export function handleFile(key, input) {
    if (input.files && input.files.length > 0) {
        state.files[key] = input.files[0];
        updateFileUI(key, state.files[key]);
    }

    updateButtons(state.files);
}

/**
 * inicializa el comportamiento de arrastrar y soltar para las zonas de archivos
 */
export function initDragAndDrop() {
    const zones = document.querySelectorAll('.drop');

    zones.forEach(zone => {
        const key = zone.id.replace('zone-', '');

        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });

        zone.addEventListener('dragleave', () => {
            zone.classList.remove('dragover');
        });

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');

            const file = e.dataTransfer.files[0];
            if (!file) return;

            const input = document.getElementById('inp-' + key);

            // sincroniza el input con el archivo soltado
            const dt = new DataTransfer();
            dt.items.add(file);
            input.files = dt.files;

            // dispara el flujo de actualización
            handleFile(key, input);
        });
    });
}