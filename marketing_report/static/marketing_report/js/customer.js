'use strict'

import {fetchJsonData} from "./func/fetchJsonData.js";

const reportButton = document.querySelector('.report-button');
const exportButton = document.querySelector('.btn-export');
const reportDate = document.querySelector('.current-date');
const years = document.querySelector('.years');
const block = document.querySelector('.cust__content');
const searchInput = document.querySelector('.dict-block__form-input');

reportButton.addEventListener('click', async e => {
    e.preventDefault();
    const rowCurrent = document.querySelector('#customer-0');
    block.querySelectorAll('.cust__row').forEach(row =>{
        if(!row.classList.contains('dict-block__row_hidden')){
            row.remove();
        }
    });
    await appendCustomerRows(rowCurrent, 'default', 0);
});

block.addEventListener('mouseover', async e => {
    const lastRecord = block.querySelector('div[data-last]:not([data-last = ""])')
    if (lastRecord) {
        const idNo = lastRecord.dataset.last;
        if (e.target === lastRecord) {
            let searchString = normalizeSearch();
            if (!searchString) {
                searchString = '';
            }
            await appendCustomerRows(lastRecord, searchString, idNo);
        }
    }
});

exportButton.addEventListener('click', () => exportFile());


/**
 * Append 50 rows after current row fetch from db
 * fetch url of dictionary_json from dictionary.py
 * @param rowCurrent — current row with last-id != '' after which append records
 * @param searchString — string to search
 * @returns {Promise<void>} array of Html elements added
 */
export async function appendCustomerRows(rowCurrent, searchString, idNo) {
    let lastRecord = rowCurrent.dataset.last
    if (!lastRecord) {
        lastRecord = 0;
    }
    const blockContent = document.querySelector('.cust__content');
    delete rowCurrent.dataset.last;
    let newRow;
    const rowCopy = blockContent.querySelector('.dict-block__row_hidden');
    const jsonUrl = `/marketing/customers_current/${reportDate.value}/${years.value}/${searchString}/${idNo}`;
    const nextRecords = await fetchJsonData(jsonUrl);
    let i = 0;
    const newRows = [];
    for (const record of nextRecords) {
        i++;
        newRow = rowCopy.cloneNode(true);
        fillCustomerRow(record, newRow);
        newRow.classList.remove('dict-block__row_hidden');
        if (i === 50) {
            newRow.dataset.last = Number.parseInt(lastRecord) + 50;
        }
        blockContent.appendChild(newRow);
        newRows.push(newRow);
    }
    return newRows;
}

/**
 * Fills the row with data from object fetched from DB
 * @param record — object from dictionary DB
 * @param newRow — row to show with fetched data
 * @returns {Promise<void>}
 */
function fillCustomerRow(record, newRow) {
    const newRowElements = newRow.querySelectorAll('div[data-field]:not([data-field = ""])');
    for (const rowElement of newRowElements) {
        const fieldName = rowElement.dataset.field;
        rowElement.textContent = record[fieldName];
    }
}

function normalizeSearch() {
    let searchString = '';
    if (searchInput) {
        searchString = searchInput.value.replace(' ', '_');
    }
    if (searchString === '') {
        searchString = 'default';
    }
    return searchString;
}

function exportFile() {
    const form = document.querySelector('#export-form');
    form.querySelector('#years').value = years.value;
    form.querySelector('#date').value = reportDate.value;
    form.submit();
}
