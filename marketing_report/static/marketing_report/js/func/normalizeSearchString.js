'use strict'

/**
 * if search string empty returns 'default'
 * @param record — row from which ou catch search window
 * @returns {string} — returns search sting or 'default'
 */
export function normalizeSearchString(record) {
    let searchString = '';
    if (record.closest('.dict-block').querySelector('.dict-block__form-input')) {
        searchString = record.closest('.dict-block').querySelector('.dict-block__form-input').value;
    }
    if (searchString === '') {
        searchString = 'default';
    }
    return searchString;
}