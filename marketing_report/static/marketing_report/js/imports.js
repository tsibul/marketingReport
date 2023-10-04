function importFileModalClose(element) {
    const modal = element.closest('#import-file-modal');
    modal.classList.remove('import-file-modal_open');
    setTimeout(() => {
        modal.style.display = 'none';
        modal.querySelector('#file-name').value = '';
        modal.querySelector('.import-file-modal__header').textContent = 'Что-то пошло не так';
    }, 250);
}

function importFileModal(thisButton, fileName) {
    const header = thisButton.closest('.form-row__export').querySelector('.import-block__description');
    const modal = document.getElementById('import-file-modal');
    modal.querySelector('#file-name').value = fileName;
    modal.style.display = 'block';
    modal.querySelector('.import-file-modal__header').textContent = header.textContent;
    setTimeout(() => {
        modal.classList.add('import-file-modal_open');
    }, 0);
}