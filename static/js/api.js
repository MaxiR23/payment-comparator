// INFO: gestiona la comunicación con la API del backend
import { state } from './state.js';
import {
    setStatus,
    showLoading,
    resetRunButton,
    showResults,
    hideResults,
    bindDownload,
    updateButtons,
    resetFileUI,
    clearStatus
} from './ui.js';

export async function runCompare() {
    showLoading();
    hideResults();
    setStatus('Subiendo archivos y comparando...', 'info');

    const fd = new FormData();
    fd.append('aulica', state.files.a);
    fd.append('control', state.files.c);
    fd.append('month', document.getElementById('sel-month').value);
    fd.append('year', document.getElementById('inp-year').value);
    fd.append('tolerance', document.getElementById('inp-tol').value);

    try {
        const res = await fetch('/compare', { method: 'POST', body: fd });
        const data = await res.json();

        if (!res.ok || data.error) {
            throw new Error(data.error || 'Error desconocido');
        }

        state.currentId = data.report_id;

        showResults(data);
        bindDownload(state.currentId);

        setStatus('Comparación completada. Descargá el informe abajo.', 'success');

    } catch (e) {
        setStatus('Error: ' + e.message, 'error');
    } finally {
        resetRunButton();
        updateButtons(state.files);
    }
}

export async function clearAll() {
    try {
        await fetch('/clear', { method: 'POST' });

        state.files.a = null;
        state.files.c = null;
        state.currentId = null;

        resetFileUI();
        hideResults();

        setStatus('Archivos limpiados.', 'info');
        updateButtons(state.files);

        setTimeout(clearStatus, 3000);
    } catch (e) {
        setStatus('Error al limpiar: ' + e.message, 'error');
    }
}