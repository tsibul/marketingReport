'use strict'

import {fillLines} from "./fillLines.js";
import {dictList} from "../../const/dictList.js";
import {fetchJsonData} from "../fetchJsonData.js";

export async function selectFromList(obj) {
    const parentDropdown = obj.closest('.dropdown');
    const parentForm = parentDropdown.closest('form');
    const inputName = parentDropdown.querySelector('.dropdown__hidden').name;
    const dataFilter = parentForm.querySelector(`[data-filter="${inputName}"]`);
    parentDropdown.querySelector('.dropdown__input').value = obj.textContent.trim().replace(/\s+/g, ' ');
    parentDropdown.querySelector('.dropdown__input').dataset.value = obj.textContent.trim().replace(/\s+/g, ' ');
    parentDropdown.querySelector('.dropdown__hidden').value = obj.dataset.value;
    obj.parentElement.classList.remove('visible');
    if (dataFilter) {
        const filterBlock = dataFilter.closest('.report_dropdown');
        const filterBlockUl = filterBlock.querySelector('ul');
        filterBlockUl.innerHTML = '';
        dataFilter.value = '';
        const dataFilterName = dataFilter.name;
        filterBlockUl.closest('.report_dropdown').querySelector(`.dropdown__input`).value = '';
        filterBlockUl.closest('.report_dropdown').querySelector(`.dropdown__input`).dataset.value = '';
        const jsonUrl =
            `/production/dictionary_json_filter/${dictList[dataFilterName]}/${dictList[inputName]}/${Number.parseInt(obj.dataset.value)}`;
        const jsonData = await fetchJsonData(jsonUrl);
        const dictionaryList = JSON.parse(jsonData);
        fillLines(filterBlockUl, dictionaryList);
    }
}
