'use strict'

export function addReportBlock(reportType, oldId) {
    // clone block from down change ids for all elements including connected labels
    const newNode = document.getElementById('report-' + reportType).cloneNode(true)
    const newId = oldId
    newNode.id = 'report-' + newId;
    newNode.querySelectorAll('[id$="' + reportType + '"]').forEach(function (element) {
        element.id = element.id.replace(reportType, newId);
    });
    newNode.querySelectorAll('[for$="' + reportType + '"]').forEach(function (element) {
        element.setAttribute('for', element.getAttribute('for').replace(reportType, newId));
    });
    newNode.classList.add('zero-width');
    return newNode;
}
