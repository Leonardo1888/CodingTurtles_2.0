document.addEventListener('DOMContentLoaded', function(){
    // Riferimenti ai modali Bootstrap
    const addModal = new bootstrap.Modal(document.getElementById('addSalaModal'));
    const editModal = new bootstrap.Modal(document.getElementById('editSalaModal'));
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteSalaModal'));
    let currentDeleteSala = null;

    // Form Aggiungi Submit
    const addSalaForm = document.getElementById('addSalaForm');
    if(addSalaForm) {
        addSalaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const data = {
                codice: document.getElementById('add-form-codice').value,
                nome: document.getElementById('add-form-nome').value,
                tema: document.getElementById('add-form-tema').value,
                mq: document.getElementById('add-form-mq').value
            };

            const headers = {'Content-Type': 'application/json'};
            const csrftoken = getCSRFToken();
            if(csrftoken) headers['X-CSRFToken'] = csrftoken;

            fetch('/sale/create/', {
                method: "POST",
                headers: headers,
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(res => {
                if(res.success) {
                    addModal.hide();
                    showToast(res.message || 'Aggiunta avvenuta', 'success');
                    // reload after short delay so user sees toast
                    setTimeout(function(){ window.location.reload(); }, 1500);
                } else {
                    showToast(res.message || 'Errore', 'danger');
                }
            })
            .catch(err => showToast('Errore di rete: ' + err, 'danger'));
        });
    }

    // Helper to get CSRF token safely (may be absent if view is csrf_exempt)
    function getCSRFToken() {
        const el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : null;
    }

    // Notification helper: creates and shows an inline dismissible alert in #notification-area
    function showToast(message, type = 'success', title = '') {
        const container = document.getElementById('notification-area');
        if(!container) {
            // If the page doesn't have the notification area, do nothing (no alert())
            return;
        }

        const id = 'notif-' + Date.now();
        const cls = (type === 'success') ? 'alert alert-success' : 'alert alert-danger';
        const html = `
            <div id="${id}" class="${cls} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;

        container.insertAdjacentHTML('beforeend', html);
        // Auto-dismiss after 3s
        setTimeout(function() {
            const el = document.getElementById(id);
            if(!el) return;
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
                bsAlert.close();
            } catch (e) {
                try { el.remove(); } catch (e) {}
            }
        }, 5000);
    }

    // Form Modifica Submit
    const editSalaForm = document.getElementById('editSalaForm');
    if(editSalaForm) {
        editSalaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const data = {
                codice: document.getElementById('edit-form-codice').value,
                nome: document.getElementById('edit-form-nome').value,
                tema: document.getElementById('edit-form-tema').value,
                mq: document.getElementById('edit-form-mq').value
            };

            const headers = {'Content-Type': 'application/json'};
            const csrftoken = getCSRFToken();
            if(csrftoken) headers['X-CSRFToken'] = csrftoken;

            fetch('/sale/update/', {
                method: "POST",
                headers: headers,
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(res => {
                if(res.success) {
                    // close modal
                    try { editModal.hide(); } catch (e) { /* ignore */ }
                    // update table row in-place (find by codice in first column)
                    const codice = data.codice;
                    const rows = document.querySelectorAll('#risultati-tabella-sale tr');
                    for(const r of rows) {
                        const firstTd = r.querySelector('td');
                        if(firstTd && firstTd.textContent.trim() === String(codice)) {
                            const tds = r.querySelectorAll('td');
                            if(tds.length >= 4) {
                                // ordine: codice, nome, tema, mq, ...
                                tds[1].textContent = data.nome;
                                tds[2].textContent = data.tema;
                                tds[3].textContent = data.mq;
                                // Aggiorna anche gli attributi data-* del pulsante Modifica nella stessa riga
                                try {
                                    const actionCell = r.querySelectorAll('td')[6];
                                    if(actionCell) {
                                        const editBtn = actionCell.querySelector('.btn-edit-sala');
                                        if(editBtn) {
                                            editBtn.setAttribute('data-nome', data.nome);
                                            editBtn.setAttribute('data-tema', data.tema);
                                            editBtn.setAttribute('data-mq', data.mq);
                                        }
                                    }
                                } catch (e) {
                                    // non critico se la struttura della tabella cambia
                                }
                            }
                            break;
                        }
                    }
                    // mostra notifica di successo
                    showToast(res.message || 'Aggiornamento avvenuto', 'success');
                    setTimeout(function(){ 
                        const el = document.querySelector('.alert');
                        if(el) {
                            const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
                            bsAlert.close();
                        }
                    }, 1500);
                } else {
                    showToast(res.message || 'Errore', 'danger');
                }
            })
            .catch(err => showToast('Errore di rete: ' + err, 'danger'));
        });
    }

    // Popola il modale di modifica quando viene mostrato (usa relatedTarget fornito da Bootstrap)
    const editModalEl = document.getElementById('editSalaModal');
    if(editModalEl) {
        editModalEl.addEventListener('show.bs.modal', function(event) {
            const trigger = event.relatedTarget; // elemento che ha aperto il modal
            if(!trigger) return;
            const codice = trigger.getAttribute('data-codice');
            const nome = trigger.getAttribute('data-nome');
            const tema = trigger.getAttribute('data-tema');
            const mq = trigger.getAttribute('data-mq');

            const codiceInput = document.getElementById('edit-form-codice');
            const nomeInput = document.getElementById('edit-form-nome');
            const temaInput = document.getElementById('edit-form-tema');
            const mqInput = document.getElementById('edit-form-mq');

            if(codiceInput) { codiceInput.value = codice || ''; }
            if(nomeInput) { nomeInput.value = nome || ''; }
            if(temaInput) { temaInput.value = tema || ''; }
            if(mqInput) { mqInput.value = mq || ''; }
        });
    }
    
    // NOTE: no click-fallback here — populating is handled by show.bs.modal

    // Elimina
    document.querySelectorAll('.btn-delete-sala').forEach(function(btn) {
        btn.addEventListener('click', function() {
            currentDeleteSala = btn.getAttribute('data-codice');
        });
    });

    // Conferma Eliminazione
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    if(confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function() {
            if(currentDeleteSala) {
                const headers = {'Content-Type': 'application/json'};
                const csrftoken = getCSRFToken();
                if(csrftoken) headers['X-CSRFToken'] = csrftoken;
                fetch('/sale/delete/', {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify({codice: currentDeleteSala})
                })
                .then(response => response.json())
                .then(res => {
                    if(res.success) {
                        deleteModal.hide();
                        showToast(res.message || 'Eliminazione avvenuta', 'success');
                        setTimeout(function(){ window.location.reload(); }, 1500);
                    } else {
                        showToast(res.message || 'Errore', 'danger');
                    }
                })
                .catch(err => showToast('Errore di rete: ' + err, 'danger'));
            }
        });
    }
});