document.addEventListener('DOMContentLoaded', function () {
    let currentSortColumn = '';
    let currentSortDirection = 'asc';
    console.log("clienti_logic.js caricato correttamente.");
    // Funzione per l'ordinamento della tabella
    window.sortTable = function (column) {
        const tbody = document.getElementById('risultati-tabella-clienti');
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

        // Mostra l’icona sulla colonna attiva
        const activeIcon = headers[columnIndex].querySelector('.sort-icon');
        if (activeIcon) activeIcon.textContent = currentSortDirection === 'asc' ? ' ▲' : ' ▼';

        // Ordina le righe
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex]?.textContent.trim() || '';
            const bValue = b.cells[columnIndex]?.textContent.trim() || '';

            // Ordine numerico per certe colonne
            if (['nAbbonamenti', 'nPrenotazioni'].includes(column)) {
                const ai = parseInt(aValue.replace(/\D/g, '')) || 0;
                const bi = parseInt(bValue.replace(/\D/g, '')) || 0;
                return currentSortDirection === 'asc' ? ai - bi : bi - ai;
            }

            return currentSortDirection === 'asc'
                ? aValue.localeCompare(bValue, undefined, { numeric: true, sensitivity: 'base' })
                : bValue.localeCompare(aValue, undefined, { numeric: true, sensitivity: 'base' });
        });

        // Aggiorna la tabella
        tbody.innerHTML = '';
        rows.forEach(r => tbody.appendChild(r));
    }
});