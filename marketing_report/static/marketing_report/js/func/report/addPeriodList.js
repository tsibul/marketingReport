'use strict'

import {periodsList} from "../reports.js";
import {selectFromList} from "../dropdown/selectFromList.js";

export function addPeriodList(newNode) {
    const periodSelect = newNode.querySelector('[id^="period-select"]')
        .parentElement.querySelector('.dropdown__content');
    let newOption;
    for (const [key, value] of Object.entries(periodsList())) {
        newOption = document.createElement('li');
        newOption.dataset.value = key;
        newOption.textContent = value;
        newOption.addEventListener('click', e => selectFromList(e.target));
        periodSelect.appendChild(newOption);
    }
}