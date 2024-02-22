'use strict'

import {selectFromList} from "./func/dropdown/selectFromList.js";
import {timeArguments, moneyArguments} from "./func/reports.js";
import {newReport} from "./func/report/newReport.js";
import {dropDownListenerVisible} from "./func/dropdown/dropDownListenerVisible.js";
import {selectFromListMod} from "./func/report/selectFromListMod.js";
import {prepareReport} from "./func/index/prepareReport.js";
import {fillReportList} from "./func/index/fillReportList.js";

const customerReport = document.querySelector('#customer-report');
const goodsReport = document.querySelector('#goods-report');
const moneyArgumentsBlock = document.querySelector('#money-arguments');
const timeArgumentsBlock = document.querySelector('#time-arguments');
const customerModal = document.querySelector('#customerModal');
const goodsModal = document.querySelector('#goodsModal');
const dropDownInput = document.querySelectorAll('.dropdown__input');
const customerModalLi = customerModal.querySelectorAll('li');
const goodsModalLi = goodsModal.querySelectorAll('li');


fillReportList();

timeArgumentsBlock.querySelectorAll('li').forEach(li => {
    li.addEventListener('click', e => selectFromList(e.target));
});
moneyArgumentsBlock.querySelectorAll('li').forEach(li => {
    li.addEventListener('click', e => selectFromList(e.target));
});

dropDownInput.forEach(dropdown => {
    const dropdownBlock = dropdown.closest('.dropdown')
    dropdown.addEventListener('click', e => dropDownListenerVisible(dropdownBlock, e));
});

goodsModalLi.forEach(li => li.addEventListener('click',
    e => selectFromListMod(e.target)));

goodsModal.querySelector('.btn-close').addEventListener('click',
    () => goodsModal.style.display = 'none')

goodsModal.querySelector('.btn-save').addEventListener('mousedown', e => prepareReport(e));

customerModalLi.forEach(li => li.addEventListener('click',
    e => selectFromListMod(e.target)));

customerModal.querySelector('.btn-close').addEventListener('click',
    () => customerModal.style.display = 'none')

customerModal.querySelector('.btn-save').addEventListener('mousedown', e => prepareReport(e));

customerReport.addEventListener('click', e => {
    customerModal.style.display = 'flex'
});
// goodsReport.addEventListener('click', e => {
//     goodsModal.style.display = 'flex'
// })


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