'use strict'

export function importFileModal(thisButton, fileName) {
    const header = thisButton.closest('.form-row__import').querySelector('.import-block__description');
    const modal = document.getElementById('import-file-modal');
    modal.querySelector('#file-name').value = fileName;
    modal.style.display = 'block';
    modal.querySelector('.import-file-modal__header').textContent = header.textContent;
    setTimeout(() => {
        modal.classList.add('import-file-modal_open');
    }, 0);
}