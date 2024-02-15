'use strict'

import {reportListRow} from "./reportListRow.js";

/**
 * fill row using report data from local storage
 */
export function fillReportList() {
    const reportListElement = document.querySelector('.report-list');
    const reportList = JSON.parse(localStorage.getItem('reports'));
    if (reportList) {
        reportList.forEach(row => {
            reportListElement.insertAdjacentElement('beforeend',
                reportListRow(row));
        });
    }
}