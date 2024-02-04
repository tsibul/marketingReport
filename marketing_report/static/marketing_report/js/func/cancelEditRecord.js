'use strict'

/**
 * Cancel edit record — remove form, remove hidden from row
 * remove blank row if there was new record
 * @param obj element of form-row
 */
export function cancelEditRecord(obj) {
    const parentObj = obj.closest('.form-row');
    const row = obj.closest('.dict-block__row');
    parentObj.remove();
    const elementId = row.dataset.id;
    if (elementId === 'e') {
        row.remove();
        return;
    }
    row.childNodes.forEach(function (element) {
        if (element.hidden) {
            element.hidden = false
        }
    });
    row.querySelector('.id-hidden').setAttribute('form', '');
}