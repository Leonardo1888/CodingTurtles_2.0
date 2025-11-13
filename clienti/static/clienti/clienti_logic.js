document.addEventListener('DOMContentLoaded', function () {
    let currentSortColumn = '';
    let currentSortDirection = 'asc';
    console.log("clienti_logic.js caricato correttamente.");

    /**
     * Funzione per l'ordinamento della tabella dei clienti.
     * @param {string} column - La colonna su cui ordinare ('codice', 'nome', ecc.).
     */
    window.sortTable = function (column) {
        const tbody = document.getElementById('risultati-tabella-clienti');
        if (!tbody) return;
        const table = tbody.closest('table');
        if (!table) return;

        const headers = Array.from(table.querySelectorAll('thead th'));

        // 1. Gestione della direzione di ordinamento e delle icone
        
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

        // 2. Ordinamento delle righe
        
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort((a, b) => {
            const cellA = a.cells[columnIndex];
            const cellB = b.cells[columnIndex];

            // Ottiene il valore testuale per l'ordinamento alfabetico/numerico standard
            const aValue = cellA?.textContent.trim() || '';
            const bValue = cellB?.textContent.trim() || '';

            // --- Logica di Ordinamento ---

            // A. Ordinamento Numerico (es. nAbbonamenti, nPrenotazioni)
            if (['nAbbonamenti', 'nPrenotazioni'].includes(column)) {
                // Estrae solo numeri (utile se la cella contiene tag <a> o altro testo)
                const ai = parseInt(aValue.replace(/[^\d]/g, '')) || 0;
                const bi = parseInt(bValue.replace(/[^\d]/g, '')) || 0;
                return currentSortDirection === 'asc' ? ai - bi : bi - ai;
            }

            // B. Ordinamento per Data (dataNas)
            if (column === 'dataNas') {
                // Usa l'attributo data-iso che DEVE contenere la data in formato YYYY-MM-DD
                const dateA_source = cellA?.dataset.iso || aValue;
                const dateB_source = cellB?.dataset.iso || bValue;
                
                // Conversione in oggetti Date
                const dA = new Date(dateA_source);
                const dB = new Date(dateB_source);

                const timeA = dA.getTime();
                const timeB = dB.getTime();
                
                // Gestione di date non valide (NaN) - le sposta in fondo
                if (isNaN(timeA) && isNaN(timeB)) return 0;
                if (isNaN(timeA)) return currentSortDirection === 'asc' ? 1 : -1;
                if (isNaN(timeB)) return currentSortDirection === 'asc' ? -1 : 1;

                const comparison = timeA - timeB;
                return currentSortDirection === 'asc' ? comparison : -comparison;
            }

            // C. Ordinamento Alfabetico/Alfanumerico (Tutte le altre colonne)
            // Usa localeCompare per l'ordinamento naturale (es. '10' dopo '2')
            const comparison = aValue.localeCompare(bValue, undefined, { numeric: true, sensitivity: 'base' });
            
            return currentSortDirection === 'asc' ? comparison : -comparison;
        });

        // 3. Aggiornamento della tabella
        tbody.innerHTML = '';
        rows.forEach(r => tbody.appendChild(r));
    }
});