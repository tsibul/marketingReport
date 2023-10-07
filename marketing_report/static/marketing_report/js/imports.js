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
    const header = thisButton.closest('.form-row__import').querySelector('.import-block__description');
    const modal = document.getElementById('import-file-modal');
    modal.querySelector('#file-name').value = fileName;
    modal.style.display = 'block';
    modal.querySelector('.import-file-modal__header').textContent = header.textContent;
    setTimeout(() => {
        modal.classList.add('import-file-modal_open');
    }, 0);
}

document.querySelector('.import-file-modal__body').addEventListener('submit', function (e) {
    e.preventDefault();
    const modal = document.getElementById('import-file-modal');
    modal.classList.remove('import-file-modal_open');
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
    // Создание объекта FormData для отправки данных формы
    const formData = new FormData(this);
    // Отправка AJAX-запроса
    fetch(this.action, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Обновление элемента с результатом
            const resultElement = document.getElementById('result');
            setTimeout(() => {
                resultElement.textContent = 'импортировано ' + data.result + ' записей';
            }, 5000);
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
});
