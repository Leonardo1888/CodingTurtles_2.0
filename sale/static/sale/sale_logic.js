document.addEventListener('DOMContentLoaded', function () {
    let currentDeleteSala = null;
    let currentSortColumn = '';
    let currentSortDirection = 'asc';

    // Funzione per l'ordinamento della tabella
    window.sortTable = function (column) {
        const tbody = document.getElementById('risultati-tabella-sale');
        if (!tbody) return;
        const table = tbody.closest('table');
        if (!table) return;

        const headers = Array.from(table.querySelectorAll('thead th'));
        headers.forEach(h => {
            const icon = h.querySelector('.sort-icon');
            if (icon) icon.textContent = '';
        });

        if (currentSortColumn === column) {
            currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            currentSortColumn = column;
            currentSortDirection = 'asc';
        }

        const columnIndex = headers.findIndex(h => h.getAttribute('data-column') === column);
        if (columnIndex === -1) return;

        const activeIcon = headers[columnIndex].querySelector('.sort-icon');
        if (activeIcon) activeIcon.textContent = currentSortDirection === 'asc' ? ' ▲' : ' ▼';

        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort((a, b) => {
            const aCell = a.cells[columnIndex];
            const bCell = b.cells[columnIndex];
            const aValue = aCell ? aCell.textContent.trim() : '';
            const bValue = bCell ? bCell.textContent.trim() : '';

            if (['mq', 'nFasceOrarie', 'nPrenotazioni'].includes(column)) {
                const ai = parseInt(aValue.replace(/\D/g, '')) || 0;
                const bi = parseInt(bValue.replace(/\D/g, '')) || 0;
                return currentSortDirection === 'asc' ? ai - bi : bi - ai;
            }

            return currentSortDirection === 'asc'
                ? aValue.localeCompare(bValue, undefined, { numeric: true, sensitivity: 'base' })
                : bValue.localeCompare(aValue, undefined, { numeric: true, sensitivity: 'base' });
        });

        tbody.innerHTML = '';
        rows.forEach(r => tbody.appendChild(r));
    };

    // Helper to get CSRF token safely
    function getCSRFToken() {
        const el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : null;
    }

    // Notification helper (mostra notifica nella navbar)
    function showToast(message, type = 'success', title = '') {
        const container = document.getElementById('notification-area');
        if (!container) return;

        const id = 'notif-' + Date.now();
        const cls = (type === 'success') ? 'alert alert-success' : 'alert alert-danger';
        const html = `
            <div id="${id}" class="${cls} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;

        container.insertAdjacentHTML('beforeend', html);

        // auto dismiss lightly later
        setTimeout(function () {
            const el = document.getElementById(id);
            if (!el) return;
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
                bsAlert.close();
            } catch (e) {
                try { el.remove(); } catch (e) { }
            }
        }, 3000);
    }

    // On load: flush stored notification (this runs after showToast is defined)
    (function flushStoredNotification() {
        try {
            const storedMsg = localStorage.getItem('salaMessage');
            const storedType = localStorage.getItem('salaType');
            if (storedMsg) {
                // show the message after the page has fully loaded
                // small timeout to ensure navbar rendered
                setTimeout(function () {
                    showToast(storedMsg, storedType || 'success');
                }, 50);
                localStorage.removeItem('salaMessage');
                localStorage.removeItem('salaType');
            }
        } catch (e) {
            console.warn('Impossibile leggere localStorage:', e);
        }
    })();


    // EVENT DELEGATION: gestione click su pulsanti Modifica / Elimina (apre i modali)
    const tbodyEl = document.getElementById('risultati-tabella-sale');
    if (tbodyEl) {
        tbodyEl.addEventListener('click', function (e) {
            const editBtn = e.target.closest('.open-edit-modal');
            if (editBtn) {
                e.preventDefault();
                closeAllModals();

                const codice = editBtn.getAttribute('data-codice') || '';
                const nome = editBtn.getAttribute('data-nome') || '';
                const tema = editBtn.getAttribute('data-tema') || '';
                const mq = editBtn.getAttribute('data-mq') || '';

                const codiceInput = document.getElementById('edit-form-codice');
                const nomeInput = document.getElementById('edit-form-nome');
                const temaInput = document.getElementById('edit-form-tema');
                const mqInput = document.getElementById('edit-form-mq');

                if (codiceInput) { codiceInput.value = codice; }
                if (nomeInput) { nomeInput.value = nome; }
                if (temaInput) { temaInput.value = tema; }
                if (mqInput) { mqInput.value = mq; }

                document.getElementById('editSalaModal').style.display = 'flex';
                return;
            }

            const deleteBtn = e.target.closest('.open-delete-modal');
            if (deleteBtn) {
                e.preventDefault();
                closeAllModals();
                currentDeleteSala = deleteBtn.getAttribute('data-codice');
                document.getElementById('deleteSalaModal').style.display = 'flex';
                return;
            }
        });
    }

    // Aggiungi SALA: submit form add
    const addSalaForm = document.getElementById('addSalaForm');
    if (addSalaForm) {
        addSalaForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const data = {
                codice: document.getElementById('add-form-codice').value,
                nome: document.getElementById('add-form-nome').value,
                tema: document.getElementById('add-form-tema').value,
                mq: document.getElementById('add-form-mq').value
            };

            const headers = { 'Content-Type': 'application/json' };
            const csrftoken = getCSRFToken();
            if (csrftoken) headers['X-CSRFToken'] = csrftoken;

            fetch('/sale/create/', {
                method: "POST",
                headers: headers,
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(res => {
                    if (res.success) {
                        // Close modals immediately
                        closeAllModals();

                        // Optional: if server returns the created row html or object in res.data,
                        // you could append it instantly here to the table so user sees it before reload.
                        // But we will perform a quick reload to get canonical state from server.
                        try {
                            localStorage.setItem('salaMessage', res.message || 'Aggiunta avvenuta');
                            localStorage.setItem('salaType', 'success');
                        } catch (e) {
                            console.warn('localStorage non disponibile:', e);
                        }

                        // fast reload (no timeouts)
                        window.location.reload();
                    } else {
                        showToast(res.message || 'Errore', 'danger');
                    }
                })
                .catch(err => showToast('Errore di rete: ' + err, 'danger'));
        });
    }

    // Edit SALA: submit form edit
    const editSalaForm = document.getElementById('editSalaForm');
    if (editSalaForm) {
        editSalaForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const data = {
                codice: document.getElementById('edit-form-codice').value,
                nome: document.getElementById('edit-form-nome').value,
                tema: document.getElementById('edit-form-tema').value,
                mq: document.getElementById('edit-form-mq').value
            };

            const headers = { 'Content-Type': 'application/json' };
            const csrftoken = getCSRFToken();
            if (csrftoken) headers['X-CSRFToken'] = csrftoken;

            fetch('/sale/update/', {
                method: "POST",
                headers: headers,
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(res => {
                    if (res.success) {
                        // Apply immediate visual update (best-effort)
                        const row = document.querySelector(`#risultati-tabella-sale tr[data-codice="${data.codice}"]`);
                        if (row) {
                            const tds = row.querySelectorAll('td');
                            if (tds.length >= 4) {
                                tds[1].textContent = data.nome;
                                tds[2].textContent = data.tema;
                                tds[3].textContent = data.mq;
                            }
                            const editBtn = row.querySelector('.open-edit-modal');
                            if (editBtn) {
                                editBtn.setAttribute('data-nome', data.nome);
                                editBtn.setAttribute('data-tema', data.tema);
                                editBtn.setAttribute('data-mq', data.mq);
                            }
                        }

                        closeAllModals();

                        try {
                            localStorage.setItem('salaMessage', res.message || 'Aggiornamento avvenuto');
                            localStorage.setItem('salaType', 'success');
                        } catch (e) {
                            console.warn('localStorage non disponibile:', e);
                        }

                        // reload quickly to reflect canonical server state
                        window.location.reload();
                    } else {
                        showToast(res.message || 'Errore', 'danger');
                    }
                })
                .catch(err => showToast('Errore di rete: ' + err, 'danger'));
        });
    }

    // Conferma Eliminazione SALA
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function () {
            if (!currentDeleteSala) {
                showToast('Nessuna sala selezionata per l\'eliminazione', 'danger');
                return;
            }
            const headers = { 'Content-Type': 'application/json' };
            const csrftoken = getCSRFToken();
            if (csrftoken) headers['X-CSRFToken'] = csrftoken;
            fetch('/sale/delete/', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({ codice: currentDeleteSala })
            })
                .then(response => response.json())
                .then(res => {
                    if (res.success) {
                        // Remove row immediately for instant feedback (best-effort)
                        const row = document.querySelector(`#risultati-tabella-sale tr[data-codice="${currentDeleteSala}"]`);
                        if (row) {
                            row.remove();
                        }

                        closeAllModals();

                        try {
                            localStorage.setItem('salaMessage', res.message || 'Eliminazione avvenuta');
                            localStorage.setItem('salaType', 'success');
                        } catch (e) {
                            console.warn('localStorage non disponibile:', e);
                        }

                        currentDeleteSala = null;
                        // quick reload
                        window.location.reload();
                    } else {
                        showToast(res.message || 'Errore', 'danger');
                    }
                })
                .catch(err => showToast('Errore di rete: ' + err, 'danger'));
        });
    }

    // Gestione modali
    function closeAllModals() {
        document.querySelectorAll('.modal-sfondo').forEach(function (modal) {
            modal.style.display = 'none';
        });
    }
    // Apri modale aggiungi sala
    document.getElementById('openAddSala').addEventListener('click', function () {
        closeAllModals();
        document.getElementById('addSalaModal').style.display = 'flex';
    });
    // Apri modale modifica sala
    document.querySelectorAll('.open-edit-modal').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            closeAllModals();
            // Popola i campi del form
            document.getElementById('edit-form-codice').value = btn.getAttribute('data-codice');
            document.getElementById('edit-form-nome').value = btn.getAttribute('data-nome');
            document.getElementById('edit-form-tema').value = btn.getAttribute('data-tema');
            document.getElementById('edit-form-mq').value = btn.getAttribute('data-mq');
            document.getElementById('editSalaModal').style.display = 'flex';
        });
    });
    // Apri modale elimina sala
    document.querySelectorAll('.open-delete-modal').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            closeAllModals();
            document.getElementById('deleteSalaModal').style.display = 'flex';
        });
    });
    // Chiudi modali
    document.querySelectorAll('.close-modal').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            closeAllModals();
        });
    });
    // Click su overlay chiude modale
    document.querySelectorAll('.modal-sfondo').forEach(function (overlay) {
        overlay.addEventListener('mousedown', function (e) {
            if (e.target === overlay) closeAllModals();
        });
    });

});
