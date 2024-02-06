'use strict'

export function changeReportBlockId(thisObj) {
    // add 1 to id for block "add report"
    const oldId = thisObj.closest('.report-block').dataset.id;
    const newId = (parseInt(oldId) + 1).toString();
    thisObj.closest('.report-block').dataset.id = newId;
    return newId;
}
