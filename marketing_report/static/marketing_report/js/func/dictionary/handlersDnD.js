'use strict'

/**
 *
 * @param event
 */
export function handleDragOver(event) {
    event.preventDefault();
}

/**
 *
 * @param event
 */
export function handleDragEnter(event) {
    const header = event.target.closest('.dict-block__header');
    if (header) {
        header.classList.add('over')
    }
}

/**
 *
 * @param event
 */
export function handleDragLeave(event) {
    const header = event.target.closest('.dict-block__header');
    if (header) {
        header.classList.remove('over')
    }
}
