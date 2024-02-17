'use strict'

import {createPeriodRow} from "../createPeriodRow.js";

export function migrationsReportBody(report) {
    const body = document.createElement('div');
    const perData = createPeriodRow(report);
    const gridClass = perData[1];
    const periodRow = perData[2];
    body.appendChild(periodRow)

    const groupDetailCurrent = document.createElement('details');
    const groupSummaryCurrent = document.createElement('summary');
    groupSummaryCurrent.classList.add('abc', gridClass, 'abc__summary');
    groupDetailCurrent.appendChild(groupSummaryCurrent);

    const companyRowCurrent = document.createElement('div');
    companyRowCurrent.classList.add('abc', gridClass, 'abc__summary');
    companyRowCurrent.insertAdjacentHTML('afterbegin', `<div></div><div></div>`);
    groupDetailCurrent.appendChild(companyRowCurrent);

    const groupDetailNew = document.createElement('details');
    const groupSummaryNew = document.createElement('summary');
    groupSummaryNew.classList.add('abc', gridClass, 'abc__summary');
    groupDetailNew.appendChild(groupSummaryNew);

    const companyRowNew = document.createElement('div');
    companyRowNew.classList.add('abc', gridClass, 'abc__summary');
    companyRowNew.insertAdjacentHTML('afterbegin', `<div></div><div></div>`);
    groupDetailNew.appendChild(companyRowNew);

    const groupDetailLost = document.createElement('details');
    const groupSummaryLost = document.createElement('summary');
    groupSummaryLost.classList.add('abc', gridClass, 'abc__summary');
    groupDetailLost.appendChild(groupSummaryLost);

    const companyRowLost = document.createElement('div');
    companyRowLost.classList.add('abc', gridClass, 'abc__summary');
    companyRowLost.insertAdjacentHTML('afterbegin', `<div></div><div></div>`);
    groupDetailLost.appendChild(companyRowLost);

    groupSummaryCurrent.insertAdjacentHTML('afterbegin',
        `<div></div><div class="abc__params">количество клиентов</div>`);
    groupSummaryNew.insertAdjacentHTML('afterbegin',
        `<div></div><div class="abc__params">новые клиенты</div>`);
    groupSummaryLost.insertAdjacentHTML('afterbegin',
        `<div></div><div class="abc__params">потеряно клиентов</div>`);


    report.report.report_data.forEach(period => {
        groupSummaryCurrent.insertAdjacentHTML('beforeend',
            `<div class="abc__digit">${period.currentQuant}</div>`);
        groupSummaryNew.insertAdjacentHTML('beforeend',
            `<div class="abc__digit">${period.newQuant}</div>`);
        groupSummaryLost.insertAdjacentHTML('beforeend',
            `<div class="abc__digit">${period.finishQuant}</div>`);
        let currentHTML = '';
        let newHTML = '';
        let lostHTML = '';
        period.customersFinished.forEach(cst => {
            lostHTML += `
                <p class="abc__migration-clients">${cst.name}</p>
                <p class="abc__migration-clients">${cst.date}</p>`
        });
        period.customersNew.forEach(cst => {
            newHTML += `
                <p class="abc__migration-clients">${cst.name}</p>
                <p class="abc__migration-clients">${cst.date}</p>`
        });
        period.customersCurrent.forEach(cst => {
            currentHTML += `
                <p class="abc__migration-clients">${cst.name}</p>
                <p class="abc__migration-clients">${cst.date}</p>`
        });
        companyRowLost.insertAdjacentHTML('beforeend', `<div>${lostHTML}</div>`);
        companyRowNew.insertAdjacentHTML('beforeend', `<div>${newHTML}</div>`);
        companyRowCurrent.insertAdjacentHTML('beforeend', `<div>${currentHTML}</div>`);
    });
    groupSummaryCurrent.insertAdjacentHTML('beforeend',
        `<div class="abc__digit">-</div>`);
    groupSummaryNew.insertAdjacentHTML('beforeend',
        `<div class="abc__digit">-</div>`);
    groupSummaryLost.insertAdjacentHTML('beforeend',
        `<div class="abc__digit">-</div>`);
    companyRowCurrent.insertAdjacentHTML('beforeend', `<div></div>`);
    companyRowNew.insertAdjacentHTML('beforeend', `<div></div>`);
    companyRowLost.insertAdjacentHTML('beforeend', `<div></div>`);
    body.appendChild(groupDetailCurrent);
    body.appendChild(groupDetailNew);
    body.appendChild(groupDetailLost);

    return body;
}