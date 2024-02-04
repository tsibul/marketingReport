'use strict'

/**
 *
 * @param node
 */
export function clearSearch(node){
    const searchInput = node.closest('.dict-block__search').querySelector('.form-input');
    searchInput.value = '';
}
