'use strict'

/**
 * Copy row from hidden row which is template for row
 * @param copyRow — original row template (hidden first line in dict html code)
 * @returns {*} — new row for editing
 */
export function copyRowFromHidden(copyRow) {
    const newRow = copyRow.cloneNode(true);
    newRow.id = newRow.id.slice(0, -1) + 'e';
    newRow.dataset.id = 'e';
    copyRow.after(newRow);
    newRow.classList.remove('dict-block__row_hidden');
    return newRow;
}
