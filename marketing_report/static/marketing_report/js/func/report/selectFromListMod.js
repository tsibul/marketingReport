'use strict'

import {selectFromList} from "../dropdown/selectFromList.js";

export async function selectFromListMod(obj) {
    const parentObj = obj.parentElement.parentElement;
    const valuePrevious = parentObj.querySelector('.dropdown__hidden').value;
    const valueCurrent = obj.dataset.value;
    await selectFromList(obj);
    const moneyReports = document.querySelector('#money-reports').value.split(',');
    const paramContent = parentObj.parentElement.querySelector('[id^="parameter-select"]')
        .parentElement.querySelector('.dropdown__content');
    let newLines;
    if (moneyReports.includes(valuePrevious) && !moneyReports.includes(valueCurrent)) {
        newLines = document.querySelector('#time-arguments');
        paramContent.innerHTML = newLines.innerHTML;
        paramContent.querySelectorAll('li')
            .forEach(li =>
                li.addEventListener('click', e => selectFromList(e.target)));
        await selectFromList(paramContent.querySelector('li'))
    } else if (!moneyReports.includes(valuePrevious) && moneyReports.includes(valueCurrent)) {
        newLines = document.querySelector('#money-arguments');
        paramContent.innerHTML = newLines.innerHTML;
        paramContent.querySelectorAll('li')
            .forEach(li =>
                li.addEventListener('click', e => selectFromList(e.target)));
        await selectFromList(paramContent.querySelector('li'))
    }
}
