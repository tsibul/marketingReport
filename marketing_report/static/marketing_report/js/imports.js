function importFileModalClose(element){
    element.closest('#import-file-modal').style.display = 'none';
}

function importFileModal(thisButton){
    const header = thisButton.closest('.form-row__export').querySelector('.import-block__description');
    const modal = document.getElementById('import-file-modal');
    modal.style.display = 'block';
    modal.querySelector('.import-file-modal__header').textContent = header.textContent;
}