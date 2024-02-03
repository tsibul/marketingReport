'use strict'

export function closeModal(click) {
    const modal = click.closest('.login');
    const inputs = modal.querySelectorAll('input');
    const textAreas = modal.querySelectorAll('textarea');
    [...inputs].forEach(e => {e.value = null});
    [...textAreas].forEach(e => {e.textContent = ''});
    modal.style.display = 'none';
}