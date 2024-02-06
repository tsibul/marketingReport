'use strict'

/**
 *
 * @param thisObj
 */
export function reportRemove(thisObj) {
    const parentObj = thisObj.parentElement.parentElement;
    parentObj.innerHTML = '';
    parentObj.classList.add('report__remove');
    setTimeout(function () {
        parentObj.remove();
    }, 295)
}