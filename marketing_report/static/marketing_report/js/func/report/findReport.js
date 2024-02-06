'use strict'

export function findReport(reportType, array) {
    const element = array.find(function (el) {
        return el['code'] === reportType
    });
    return element['description']
}
