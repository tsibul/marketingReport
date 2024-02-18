'use strict'

import {reportTitle} from "./reportTitle.js";
import {abcReportBody} from "./abc/abcReportBody.js";
import {migrationsReportBody} from "./migrations/migrationsReportBody.js";
import {geographyReportBody} from "./geography/geographyReportBody.js";
import {groupReportBody} from "./groups/groupReportBody.js";

export function createReport(e) {
    const container = document.querySelector('.full-content').querySelector('.container');
    const reportBody = document.createElement('section');
    reportBody.classList.add('report-body');
    const reportListRow = e.target.closest('.report-list__row');
    const reportId = reportListRow.querySelector('input').value;
    const reportList = JSON.parse(localStorage.getItem('reports'));
    let report;
    for (let i = 0; i < reportList.length; i++) {
        if (reportList[i].id === Number(reportId)) {
            report = reportList[i];
            break;
        }
    }
    const reportHeader = reportTitle(report);
    reportBody.appendChild(reportHeader);
    const body = chooseBody(report);
    reportBody.appendChild(body);
    container.appendChild(reportBody);
}

function chooseBody(report) {
    let body;
    switch (report.report.report_name) {
        case 'Клиенты ABC - анализ':
            body = abcReportBody(report);
            break;
        case 'Клиенты Миграции клиентов':
            body = migrationsReportBody(report);
            break;
        case 'Клиенты Типы и география':
            body = geographyReportBody(report);
            break;
        case 'Клиенты Направления бизнеса':
            body = groupReportBody(report);
            break;

    }
    return body
}
