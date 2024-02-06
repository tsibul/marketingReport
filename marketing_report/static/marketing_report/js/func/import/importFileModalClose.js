'use strict'

export function importFileModalClose(element) {
    const modal = element.closest('#import-file-modal');
    modal.classList.remove('import-file-modal_open');
    setTimeout(() => {
        modal.style.display = 'none';
        modal.querySelector('#file-name').value = '';
        modal.querySelector('.import-file-modal__header').textContent = 'Что-то пошло не так';
    }, 250);
}
