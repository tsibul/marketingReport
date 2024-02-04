'use strict'

import {fetchJsonData} from "./fetchJsonData.js";
import {dictList} from "../const/dictList.js";

/**
 * Fills the row with data from object fetched from DB
 * @param record — object from dictionary DB
 * @param i — index of record
 * @param newRow — row to show with fetched data
 * @returns {Promise<void>}
 */
export async function fillNewRow(record, i, newRow) {
    const newRowElements = newRow.querySelectorAll('div[data-field]:not([data-field = ""])');
    if (record['id']) {
        newRow.dataset.id = record['id'];
        newRow.id = newRow.id.slice(0, -1) + record['id'];
        newRow.querySelector('.id-hidden').value = record['id'];
// temporary fix for imm data for OneToOne key
//     } else if (record['imm_id']){
//         newRow.dataset.id = record['imm_id'];
//         newRow.id = newRow.id.slice(0, -1) + record['imm_id'];
//         newRow.querySelector('.id-hidden').value = record['imm_id'];
    }
    const square = newRow.querySelector('.hex');
    if (square) {
        square.style.backgroundColor = record['hex'];
    }
    if (record['date_close']) {
        newRow.classList.add('fulfilled');
        const buttons = newRow.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.setAttribute('disabled', true);
            btn.classList.add('form-input__inactive')
        });
    }

    for (const rowElement of newRowElements) {
        const fieldName = rowElement.dataset.field;
        if (rowElement.classList.contains('bool-field')) {
            rowElement.textContent = record[fieldName] ? 'Да' : 'Нет';
            rowElement.dataset.id = record[fieldName] ? '1' : '0';
        } else {
            rowElement.textContent = record[fieldName];
            if (rowElement.classList.contains('foreign-key')) {
                rowElement.dataset.id = record[fieldName + '_id'];
            }
        }
    }
}
