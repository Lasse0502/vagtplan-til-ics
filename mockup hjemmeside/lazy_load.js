
    const tableWrapper = document.querySelector('.table-wrapper');
    const tableBody = document.querySelector('.time-overview-table tbody');
    const allRows = Array.from(tableBody.rows);
    const rowHeight = allRows[0] ? allRows[0].offsetHeight : 30;
    const visibleRowCount = Math.ceil(tableWrapper.offsetHeight / rowHeight) + 5;
    const totalRowCount = allRows.length;

    function updateVisibleRows(startIndex) {
        tableBody.innerHTML = '';

        const endIndex = Math.min(startIndex + visibleRowCount, totalRowCount);
        const visibleRows = allRows.slice(startIndex, endIndex);

        const topPadding = startIndex * rowHeight;
        const bottomPadding = (totalRowCount - endIndex) * rowHeight;

        const topPaddingRow = document.createElement('tr');
        topPaddingRow.style.height = `${topPadding}px`;
        const bottomPaddingRow = document.createElement('tr');
        bottomPaddingRow.style.height = `${bottomPadding}px`;

        tableBody.appendChild(topPaddingRow);
        visibleRows.forEach(row => tableBody.appendChild(row.cloneNode(true)));
        tableBody.appendChild(bottomPaddingRow);
    }

    tableWrapper.addEventListener('scroll', function() {
        const scrollTop = tableWrapper.scrollTop;
        const startIndex = Math.floor(scrollTop / rowHeight);
        updateVisibleRows(startIndex);
    });

    // Initial indlæsning
    updateVisibleRows(0);
