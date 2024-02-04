'use strict'

import {appendNewRows} from "../appendNewRows.js";

/**
 *
 * @param eventTarget
 * @returns {Promise<void>}
 */
export async function initDictionary(eventTarget, shDeleted){
        const dictToFind = eventTarget.id + '-0';
        const dictToCopy = document.getElementById(dictToFind).closest('.dict-block');
        const dictBlockContent = dictToCopy.querySelector('.dict-block__content');
        const hiddenRow = dictToCopy.querySelector('.dict-block__row_hidden');
        const searchVal = 'default';
        const temporaryRow = hiddenRow.cloneNode(true);
        temporaryRow.setAttribute('data-last', '0');
        dictBlockContent.appendChild(temporaryRow);
        dictBlockContent.appendChild(hiddenRow);
        await appendNewRows(temporaryRow, dictBlockContent, searchVal, shDeleted, 0);
        temporaryRow.remove();
}
