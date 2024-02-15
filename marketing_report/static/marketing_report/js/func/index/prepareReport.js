'use strict'

import {fetchJsonData} from "../fetchJsonData.js";
import {reportListRow} from "./reportListRow.js";

/**
 * Collect initial data from modal
 * Fetch result from url
 * add new report to report list
 * store new report list to local storage
 * @param e
 * @returns {Promise<void>}
 */
export async function prepareReport(e) {
    const currentDate = new Date().toLocaleDateString();
    let reportList = JSON.parse(localStorage.getItem('reports'));
    let lastIndex = localStorage.getItem('reportIndex');
    if (!lastIndex) {
        lastIndex = 0;
        localStorage.setItem('reportIndex', '0');
    }
    const btn = e.target;
    const currentForm = btn.closest('.report-block_modal');
    const reportClass = currentForm.getAttribute('id').slice(0, -5);
    const reportType = currentForm.querySelector('[id^="report-select"]').value;
    const period = currentForm.querySelector('[id^="period-select"]').value;
    let yearFirst = currentForm.querySelector('.year-first').value;
    let yearLast = currentForm.querySelector('.year-last').value;
    if (yearFirst === '' || yearLast === '') {
        yearFirst = new Date().getFullYear() - 1;
        yearLast = new Date().getFullYear() - 1;
    }
    const parameter = currentForm.querySelector('[id^="parameter-select"]').value;
    currentForm.style.display = 'none';
    const url = `report/${reportClass}/${reportType}/${period}/${parameter}/${yearFirst}/${yearLast}`;
    const reportData = await fetchJsonData(url);
    lastIndex = Number(lastIndex) + 1;
    if (!reportList) {
        reportList = [{
            'id': lastIndex,
            'date': currentDate,
            'report': reportData
        }]
    } else {
        reportList.push({
            'id': lastIndex,
            'date': currentDate,
            'report': reportData
        });
    }
    localStorage.setItem('reports', JSON.stringify(reportList));
    localStorage.setItem('reportIndex', lastIndex.toString());
    const reportListElement = document.querySelector('.report-list');
    reportListElement.insertAdjacentElement('beforeend',
        reportListRow({
            'id': lastIndex,
            'date': currentDate,
            'report': reportData
        }));
}