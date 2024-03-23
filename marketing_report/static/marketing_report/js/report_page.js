'use strict'

import {selectFromList} from "./func/dropdown/selectFromList.js";
import {timeArguments, moneyArguments} from "./func/reports.js";
import {newReport} from "./func/report/newReport.js";

const customerReport = document.querySelector('#customer-report');
const goodsReport = document.querySelector('#goods-report');
const moneyArgumentsBlock = document.querySelector('#money-arguments');
const timeArgumentsBlock = document.querySelector('#time-arguments');

timeArgumentsBlock.querySelectorAll('li').forEach(li => {
    li.addEventListener('click', e => selectFromList(e.target));
});
moneyArgumentsBlock.querySelectorAll('li').forEach(li => {
    li.addEventListener('click', e => selectFromList(e.target));
});

customerReport.addEventListener('click', e => {
    newReport(e.target, 0)
});
goodsReport.addEventListener('click', e => newReport(e.target, 10000))

// change argument list
function changeArgumentList(thisObj) {
    const parentObj = thisObj.parentElement;
    let newOptions;
    if (thisObj.value === 'MIG' || thisObj.value === 'CLR') {
        newOptions = timeArguments();
        parentObj.querySelector('[for^="parameter-select"]').textContent = 'время жизни';
    } else {
        newOptions = moneyArguments();
        parentObj.querySelector('[for^="parameter-select"]').textContent = 'показатель';
    }
    const argumentSelect = parentObj.querySelector('[id^="parameter-select"]');
    argumentSelect.replaceChildren();
    let newOption;
    newOptions.forEach(function (argument) {
        newOption = document.createElement('option');
        newOption.value = argument['code'];
        newOption.textContent = argument['description'];
        argumentSelect.appendChild(newOption);
    });
    parentObj.querySelector('[for^="parameter-select"]');
}