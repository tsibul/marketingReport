'use strict'

import {customerReports, goodsReports} from "../reports.js";
import {findReport} from "./findReport.js";
import {changeHeadingStyle} from "./changeHeadingStyle.js";
import {emptyReportBlockBig} from "./emptyReportBlockBig.js";

export function buildReport(thisObj) {
    const parentObj = thisObj.parentElement.parentElement;
    const blockId = parentObj.id.split('-').pop();
    const reportNo = parseInt(blockId) < 10000 ? '0' : '10000';
    const reportType = parentObj.querySelector('[id^="report-select"]').value;
    const reportTitle = reportNo === '0' ? 'Клиенты. ' + findReport(reportType, customerReports())
        : 'Товары. ' + findReport(reportType, goodsReports());
    const period = parentObj.querySelector('[id^="period-select"]').value;
    const dates = parentObj.querySelectorAll('[type="date"]');
    const dateBegin = dates[0].value;
    const dateEnd = dates[1].value;
    const argument = parentObj.querySelector('[id^="parameter-select"]').value;
    if (dateBegin !== '' && dateEnd !== '' && dateBegin < dateEnd) {
        changeHeadingStyle(parentObj);
        emptyReportBlockBig(parentObj, reportTitle);
    } else if (dateBegin === '') {
        dates[0].focus();
    } else {
        dates[1].focus();
    }
}
