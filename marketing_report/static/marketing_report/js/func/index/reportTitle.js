'use strict'

export function reportTitle(report) {
    const row = document.createElement('div');
    row.classList.add('report-body__title');
    const rowContent = `
                <div>${report.report.report_name}</div>
                <div>дата отч.&nbsp;${report.date}</div>
                <div>детализация&nbsp;${report.report.period}</div>
                <div>c&nbsp;${report.report.date_begin}</div>
                <div>по&nbsp;${report.report.date_end}</div>
                <div>параметр:&nbsp;${report.report.parameter}</div>
                <button type="button" class="btn btn-save">закрыть</button>`;
    row.insertAdjacentHTML('afterbegin', rowContent);
    const buttonClose = row.querySelector('.btn');
    buttonClose.addEventListener('click', () => {
        const reportBody = buttonClose.closest('.report-body');
        reportBody.remove();
    });
    return row;
}