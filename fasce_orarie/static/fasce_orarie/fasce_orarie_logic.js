document.addEventListener('DOMContentLoaded', function () {
    let currentSortColumn = '';
    let currentSortDirection = 'asc';
    console.log("fasce_orarie_logic.js caricato correttamente.");

    /**
     * Ordina le righe della tabella in base alla colonna specificata.
     * @param {string} column L'attributo data-column dell'intestazione (es. 'sala', 'data', 'ora', 'durata').
     */
    window.sortTable = function (column) {
        const tbody = document.getElementById('risultati-tabella-fasce_orarie');
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

            let comparison = 0;

            if (column === 'durata') {
                // Ordine numerico per la Durata
                const ai = parseInt(aValue) || 0;
                const bi = parseInt(bValue) || 0;
                comparison = ai - bi;
            } else if (column === 'data' || column === 'ora') {
                // Ordine cronologico/temporale per Data e Ora
                comparison = aValue.localeCompare(bValue);
            } else {
                // Ordine alfanumerico standard per Codice Sala
                comparison = aValue.localeCompare(bValue, undefined, { numeric: true, sensitivity: 'base' });
            }

            // Applica la direzione di ordinamento
            return currentSortDirection === 'asc' ? comparison : -comparison;
        });

        // Aggiorna la tabella
        tbody.innerHTML = '';
        rows.forEach(r => tbody.appendChild(r));
    }
});