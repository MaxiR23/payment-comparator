// INFO: maneja todas las actualizaciones del DOM y el estado de la interfaz de usuario
export function updateFileUI(key, file) {
    const zone = document.getElementById('zone-' + key);
    const lbl  = document.getElementById('lbl-' + key);

    if (file) {
        zone.classList.add('loaded');
        const n = file.name;
        lbl.textContent = n.length > 22 ? n.slice(0, 20) + '…' : n;
    }
}

export function resetFileUI() {
    document.getElementById('zone-a').classList.remove('loaded');
    document.getElementById('zone-c').classList.remove('loaded');

    document.getElementById('lbl-a').textContent = 'Archivo Áulica';
    document.getElementById('lbl-c').textContent = 'Planilla Control';

    document.getElementById('inp-a').value = '';
    document.getElementById('inp-c').value = '';
}

export function updateButtons(files) {
    const ready = files.a && files.c;

    document.getElementById('btn-run').disabled   = !ready;
    document.getElementById('btn-clear').disabled = !(files.a || files.c);
}

export function setStatus(msg, type) {
    const el = document.getElementById('status');
    el.className = 'status ' + type;
    el.innerHTML = msg;
}

export function showLoading() {
    const btn = document.getElementById('btn-run');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Procesando...';
}

export function resetRunButton() {
    const btn = document.getElementById('btn-run');
    btn.disabled = false;
    btn.textContent = 'Comparar archivos';
}

export function showResults(data) {
    document.getElementById('v-dif').textContent  = data.n_diffs;
    document.getElementById('v-falt').textContent = data.n_ctrl_only;
    document.getElementById('v-total').textContent =
        '$' + data.total_diff.toLocaleString('es-AR', { minimumFractionDigits: 2 });

    document.getElementById('results').style.display = 'block';
}

export function hideResults() {
    document.getElementById('results').style.display = 'none';
}

export function bindDownload(id) {
    document.getElementById('btn-dl').onclick = () => {
        window.location = '/download/' + id;
    };
}

export function clearStatus() {
    const el = document.getElementById('status');
    el.innerHTML = '';
    el.className = 'status';
}