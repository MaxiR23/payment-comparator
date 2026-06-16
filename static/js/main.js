// INFO: punto de entrada - conecta eventos y módulos
import { handleFile, initDragAndDrop } from './files.js';
import { runCompare, clearAll } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('dragover', (e) => e.preventDefault());
    
    document.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation(); 
    });

    // archivos
    document.getElementById('inp-a').addEventListener('change', (e) => handleFile('a', e.target));
    document.getElementById('inp-c').addEventListener('change', (e) => handleFile('c', e.target));

    // botones
    document.getElementById('btn-run').addEventListener('click', runCompare);
    document.getElementById('btn-clear').addEventListener('click', clearAll);

    initDragAndDrop();
});