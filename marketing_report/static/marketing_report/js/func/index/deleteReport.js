'use strict'

/**
 * Delete report from prepared report list & localStorage
 * @param btn - btn-delete
 */
export function deleteReport(e) {
    e.stopPropagation();
    const btn = e.target;
    const row = btn.closest('.report-list__row');
    const reportId = row.querySelector('input').value;
    row.remove()
    let reportList = JSON.parse(localStorage.getItem('reports'));
    for (let i = 0; i < reportList.length; i++) {
        if (reportList[i].id === Number(reportId)) {
            reportList.splice(i, 1);
            break;
        }
    }
    localStorage.setItem('reports', JSON.stringify(reportList));
}