'use strict'

/**
 * function for search button
 * @param block — block from which ou catch search window
 * @returns {*} — returns search sting or 'default'
 */
export function normalizeSearchStringValue(block) {
    const searchString = block.querySelector('.form-input').value;
    let searchValue;
    if (searchString === '') {
        searchValue = 'default';
    } else {
        searchValue = searchString.replaceAll(/  +/g, ' ').replaceAll(' ', '_')
    }
    return searchValue;
}