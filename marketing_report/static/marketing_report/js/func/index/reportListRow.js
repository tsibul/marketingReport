'use strict'

import {deleteReport} from "./deleteReport.js";
import {createReport} from "./createReport.js";

/**
 * Make row in prepared row list from report data taken from local storage or new report
 * create eventListener on delete button
 * @param report - report data taken from local storage or new report
 * @returns {HTMLDivElement} - row in row list
 */
export function reportListRow(report) {
    const row = document.createElement('div');
    row.classList.add('report-list__row');
    const rowContent = `
                <input type="text" value="${report.id}" hidden>
                <div>${report.date}</div>
                <div>${report.report.report_name}</div>
                <div>${report.report.period}</div>
                <div>c&nbsp;${report.report.date_begin}</div>
                <div>по&nbsp;${report.report.date_end}</div>
                <div>cортировка&nbsp;${report.report.parameter}</div>
                <button type="button" class="btn btn-save">удалить</button>`;
    row.insertAdjacentHTML('afterbegin', rowContent);
    row.querySelector('.btn').addEventListener('click', e => deleteReport(e));
    row.addEventListener('click', e => createReport(e));
    return row;
}