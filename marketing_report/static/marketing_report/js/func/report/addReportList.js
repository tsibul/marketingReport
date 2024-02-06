'use strict'

import {customerReports, goodsReports} from "../reports.js";
import {selectFromListMod} from "./selectFromListMod.js";

export function addReportList(newNode, reportType) {
    const reportSelect = newNode.querySelector('[id^="report-select"]')
        .parentElement.querySelector('.dropdown__content');
    const reportArray = reportType === 0 ? customerReports() : goodsReports();
    let newOption;
    reportArray.forEach(function (report) {
        newOption = document.createElement('li');
        newOption.dataset.value = report['code'];
        newOption.textContent = report['description'];
        newOption.addEventListener('click', e => selectFromListMod(e.target));
        reportSelect.appendChild(newOption);
    });
}