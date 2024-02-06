'use strict'

import {typeDict} from "./typeDict.js";
import {fetchJsonData} from "./fetchJsonData.js";
import {fillNewRow} from "./fillNewRow.js";

/**
 * Append 20 rows after current row fetch from db
 * fetch url of dictionary_json from dictionary.py
 * @param rowCurrent — current row with last-id != '' after which append records
 * @param blockContent — content block of current dictionary
 * @param searchString — string to search
 * @param shDeleted — parameter if show deleted records
 * @param unclosed — parameter show closed/unclosed records
 * @returns {Promise<void>} array of Html elements added
 */
export async function appendNewRows(rowCurrent, blockContent, searchString, shDeleted, unclosed) {
    const lastRecord = rowCurrent.dataset.last
    delete rowCurrent.dataset.last;
    let newRow;
    const rowCopy = blockContent.querySelector('.dict-block__row_hidden');
    const dictType = typeDict(rowCurrent);
    const jsonUrl = `/marketing/json_dict_next_20/${dictType}/${lastRecord}/default/${searchString}/${shDeleted}`;
    const nextRecords = await fetchJsonData(jsonUrl);
    let i = 0;
    const newRows = [];
    for (const record of nextRecords) {
        i++;
        newRow = rowCopy.cloneNode(true);
        await fillNewRow(record, i, newRow);
        newRow.classList.remove('dict-block__row_hidden');
        if (i === 20) {
            newRow.dataset.last = Number.parseInt(lastRecord) + 20;
        }
        blockContent.appendChild(newRow);
        newRows.push(newRow);
    }
    return newRows;
}