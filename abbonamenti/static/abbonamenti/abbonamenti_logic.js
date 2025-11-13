document.addEventListener('DOMContentLoaded', function () {
    let currentSortColumn = '';
    let currentSortDirection = 'asc';
    console.log("abbonamenti_logic.js caricato correttamente.");
    
    // Funzione per l'ordinamento della tabella
    window.sortTable = function (column) {
        const tbody = document.getElementById('risultati-tabella-abbonamenti');
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

        // Mostra l'icona sulla colonna attiva
        const activeIcon = headers[columnIndex].querySelector('.sort-icon');
        if (activeIcon) activeIcon.textContent = currentSortDirection === 'asc' ? ' ▲' : ' ▼';

        // Ordina le righe
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex]?.textContent.trim() || '';
            const bValue = b.cells[columnIndex]?.textContent.trim() || '';

            // Ordine numerico per colonne specifiche degli abbonamenti
            if (['nAbb', 'prezzo'].includes(column)) {
                const ai = parseFloat(aValue.replace(/[^\d.-]/g, '')) || 0;
                const bi = parseFloat(bValue.replace(/[^\d.-]/g, '')) || 0;
                return currentSortDirection === 'asc' ? ai - bi : bi - ai;
            }

            if (column === 'inizio') {
                // Modifica qui: cerca prima l'attributo data-iso, altrimenti usa il testo della cella
                const dateA_source = a.cells[columnIndex]?.dataset.iso || aValue;
                const dateB_source = b.cells[columnIndex]?.dataset.iso || bValue;
                
                // Il formato ISO 'yyyy-mm-dd' è riconosciuto correttamente da new Date()
                const dA = new Date(dateA_source);
                const dB = new Date(dateB_source);

                const timeA = dA.getTime();
                const timeB = dB.getTime();

                if (isNaN(timeA) && isNaN(timeB)) return 0;
                if (isNaN(timeA)) return currentSortDirection === 'asc' ? 1 : -1;
                if (isNaN(timeB)) return currentSortDirection === 'asc' ? -1 : 1;

                const comparison = timeA - timeB;
                return currentSortDirection === 'asc' ? comparison : -comparison;
            }

            if (column === 'fine') {
                // Modifica qui: cerca prima l'attributo data-iso, altrimenti usa il testo della cella
                const dateA_source = a.cells[columnIndex]?.dataset.iso || aValue;
                const dateB_source = b.cells[columnIndex]?.dataset.iso || bValue;
                
                // Il formato ISO 'yyyy-mm-dd' è riconosciuto correttamente da new Date()
                const dA = new Date(dateA_source);
                const dB = new Date(dateB_source);

                const timeA = dA.getTime();
                const timeB = dB.getTime();

                if (isNaN(timeA) && isNaN(timeB)) return 0;
                if (isNaN(timeA)) return currentSortDirection === 'asc' ? 1 : -1;
                if (isNaN(timeB)) return currentSortDirection === 'asc' ? -1 : 1;

                const comparison = timeA - timeB;
                return currentSortDirection === 'asc' ? comparison : -comparison;
            }

            // Ordine alfabetico per le altre colonne
            return currentSortDirection === 'asc'
                ? aValue.localeCompare(bValue, undefined, { numeric: true, sensitivity: 'base' })
                : bValue.localeCompare(aValue, undefined, { numeric: true, sensitivity: 'base' });
        });

        // Aggiorna la tabella
        tbody.innerHTML = '';
        rows.forEach(r => tbody.appendChild(r));
    }
});