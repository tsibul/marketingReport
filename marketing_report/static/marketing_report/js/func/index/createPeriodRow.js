'use strict'

export function createPeriodRow(report) {
    const periodData = report.report.period_data;
    const periodDataLength = periodData.length;
    const gridClass = 'abc__' + periodDataLength;
    const periodRow = document.createElement('div');
    periodRow.classList.add('abc', gridClass, 'active');
    periodRow.insertAdjacentHTML('afterbegin',
        `<div>название</div><div>показатели</div>`);
    periodData.forEach(per => {
        let period = document.createElement('div');
        period.textContent = per.name;
        period.classList.add('abc__digit');
        periodRow.appendChild(period);
    });
    periodRow.insertAdjacentHTML('beforeend',
        `<div class="abc__digit">всего</div>`);
    return[periodData, gridClass, periodRow];

}