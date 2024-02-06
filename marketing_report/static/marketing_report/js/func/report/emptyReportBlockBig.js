'use strict'

export function emptyReportBlockBig(parentObj, reportTitle) {
    parentObj.classList.add('report-long');
    const reportHeading = parentObj.querySelector('.border-title')
    reportHeading.textContent = reportTitle;
    const dateRow = parentObj.querySelector('.date-row').cloneNode(true);
    const reportSelector = parentObj.querySelector('[id^="report-select"]').parentElement.cloneNode(true);
    reportSelector.value = parentObj.querySelector('[id^="report-select"]').value;
    reportSelector.style.display = 'none';
    const periodSelector = parentObj.querySelector('[id^="period-select"]').parentElement.cloneNode(true);
    periodSelector.value = parentObj.querySelector('[id^="period-select"]').value;
    periodSelector.classList.add('report-long_period');
    const argumentSelector = parentObj.querySelector('[id^="parameter-select"]').parentElement.cloneNode(true);
    argumentSelector.value = parentObj.querySelector('[id^="parameter-select"]').value;
    argumentSelector.classList.add('report-long_parameter');
    const periodText = document.createElement('label');
    periodText.textContent = ' детализация ';
    periodText.setAttribute('for', periodSelector.id);
    const argumentText = document.createElement('label');
    argumentText.textContent = ' показатель ';
    argumentText.setAttribute('for', argumentSelector.id);

    parentObj.querySelector('.report-block-content').innerHTML = '';
    parentObj.querySelector('.report-header').replaceChildren(reportHeading, dateRow, argumentText, argumentSelector, periodText, periodSelector, reportSelector);
}
