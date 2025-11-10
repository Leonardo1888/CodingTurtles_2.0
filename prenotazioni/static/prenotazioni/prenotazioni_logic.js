document.addEventListener('DOMContentLoaded', function () {
    let currentSortColumn = '';
    let currentSortDirection = 'asc';
    console.log("prenotazioni_logic.js caricato correttamente.");

    // Funzione per l'ordinamento della tabella delle prenotazioni
    window.sortTable = function (column) {
        const tbody = document.getElementById('risultati-tabella-prenotazioni');
        if (!tbody) return;
        const table = tbody.closest('table');
        if (!table) return;

        const headers = Array.from(table.querySelectorAll('thead th'));

        // Rimuove le frecce da tutte le colonne
        headers.forEach(h => {
            const icon = h.querySelector('.sort-icon');
            if (icon) icon.textContent = '';
        });

        // Inverte la direzione o imposta ascendente
        if (currentSortColumn === column) {
            currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            currentSortColumn = column;
            currentSortDirection = 'asc';
        }

        const columnIndex = headers.findIndex(h => h.getAttribute('data-column') === column);
        if (columnIndex === -1) return;

        // Mostra l'icona sulla colonna attiva (se presente)
        const activeIcon = headers[columnIndex]?.querySelector('.sort-icon');
        if (activeIcon) activeIcon.textContent = currentSortDirection === 'asc' ? ' ▲' : ' ▼';

        // Ordina le righe
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex]?.textContent.trim() || '';
            const bValue = b.cells[columnIndex]?.textContent.trim() || '';

            // Colonne numeriche o con codici
            if (['cliente', 'sala', 'posto', 'abbonamento'].includes(column)) {
                return currentSortDirection === 'asc'
                    ? aValue.localeCompare(bValue, undefined, { numeric: true, sensitivity: 'base' })
                    : bValue.localeCompare(aValue, undefined, { numeric: true, sensitivity: 'base' });
            }

            // Colonne data/ora
            if (column === 'data') {
                const dateA = new Date(aValue);
                const dateB = new Date(bValue);
                if (!isNaN(dateA) && !isNaN(dateB)) {
                    return currentSortDirection === 'asc' ? dateA - dateB : dateB - dateA;
                }
            }

            if (column === 'ora') {
                const timeA = aValue.split(':').map(Number);
                const timeB = bValue.split(':').map(Number);
                const minutesA = (timeA[0] || 0) * 60 + (timeA[1] || 0);
                const minutesB = (timeB[0] || 0) * 60 + (timeB[1] || 0);
                return currentSortDirection === 'asc' ? minutesA - minutesB : minutesB - minutesA;
            }

            return 0;
        });

        // Aggiorna la tabella
        tbody.innerHTML = '';
        rows.forEach(r => tbody.appendChild(r));
    }
});
