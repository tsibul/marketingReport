'use strict'

import {selectFromList} from "./selectFromList.js";

/**
 *
 * @param ulContent
 * @param dictionaryList
 */
export function fillLines(ulContent, dictionaryList) {
    let newLine;
    dictionaryList.forEach(elem => {
        newLine = document.createElement('li');
        newLine.onclick = async function (event) {
            event.stopPropagation();
            await selectFromList(event.target);
        };
        newLine.dataset.value = Object.keys(elem)[0];
        newLine.textContent = Object.values(elem)[0];
        ulContent.appendChild(newLine);
    });
}