document.addEventListener('DOMContentLoaded', function () {
    let currentSortColumn = '';
    let currentSortDirection = 'asc';
    console.log("prenotazioni_logic.js caricato correttamente.");

    window.sortTable = function (column) {
        const tbody = document.getElementById('risultati-tabella-prenotazioni');
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

        const activeIcon = headers[columnIndex]?.querySelector('.sort-icon');
        if (activeIcon) activeIcon.textContent = currentSortDirection === 'asc' ? ' ▲' : ' ▼';

        const rows = Array.from(tbody.querySelectorAll('tr'));

        const monthMap = {
            "gennaio": 0, "febbraio": 1, "marzo": 2, "aprile": 3,
            "maggio": 4, "giugno": 5, "luglio": 6, "agosto": 7,
            "settembre": 8, "ottobre": 9, "novembre": 10, "dicembre": 11
        };

        function parseItalianDate(str) {
            if (!str) return null;
            // normalizza spazi, rimuove caratteri non necessari
            const s = str.trim().toLowerCase().replace(/\u00A0/g, ' ').replace(/\./g, '').replace(/°/g, '');
            // se formato dd/mm/yyyy o d/m/yyyy
            if (/^\d{1,2}\s*\/\s*\d{1,2}\s*\/\s*\d{4}$/.test(s)) {
                const parts = s.split('/').map(p => p.trim());
                const day = parseInt(parts[0], 10);
                const month = parseInt(parts[1], 10) - 1;
                const year = parseInt(parts[2], 10);
                if (!isNaN(day) && !isNaN(month) && !isNaN(year)) return new Date(year, month, day);
            }
            // split su qualunque quantità di spazi
            const parts = s.split(/\s+/);
            // possibili formati: ['01','giugno','2025'] oppure ['1','giugno','2025']
            if (parts.length >= 3) {
                const day = parseInt(parts[0].replace(/[^\d]/g, ''), 10);
                const monthName = parts[1];
                const year = parseInt(parts[2].replace(/[^\d]/g, ''), 10);
                const month = monthMap[monthName];
                if (!isNaN(day) && month !== undefined && !isNaN(year)) {
                    return new Date(year, month, day);
                }
            }
            return null;
        }

        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex]?.textContent.trim() || '';
            const bValue = b.cells[columnIndex]?.textContent.trim() || '';

            if (['cliente', 'sala', 'posto', 'abbonamento'].includes(column)) {
                return currentSortDirection === 'asc'
                    ? aValue.localeCompare(bValue, undefined, { numeric: true, sensitivity: 'base' })
                    : bValue.localeCompare(aValue, undefined, { numeric: true, sensitivity: 'base' });
            }

            if (column === 'data') {
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

            if (column === 'ora') {
                const timeA = aValue.split(':').map(Number);
                const timeB = bValue.split(':').map(Number);
                const minutesA = (timeA[0] || 0) * 60 + (timeA[1] || 0);
                const minutesB = (timeB[0] || 0) * 60 + (timeB[1] || 0);
                return currentSortDirection === 'asc' ? minutesA - minutesB : minutesB - minutesA;
            }

            return 0;
        });

        tbody.innerHTML = '';
        rows.forEach(r => tbody.appendChild(r));
    }
});
