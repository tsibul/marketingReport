const buttonClose = document.querySelector('.modal.close');

// buttonClose.onclick(buttonClose => importFileModalClose(buttonClose));

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

async function editTemporaryBase() {
    const counts = await fetchJsonData('/marketing/edit_temporary_base');
    console.log(counts)
    const newCustomers = document.getElementById('new-customers');
    const updatedCustomers = document.getElementById('updated-customers');
    newCustomers.textContent = `новые ${counts.new_customers}`;
    updatedCustomers.textContent = `измененные ${counts.updated_customers}`;
}

async function importCustomers(url) {
    const counts = await fetchJsonData('/marketing/' + url);
    const newCustomers = document.getElementById(url);
    newCustomers.textContent = `импортировано ${counts.result}`;
}


function reassignPeriods(button) {
    button.preventDefault();
    const currentForm = this.closest('form')
    const dateBeginPrev = currentForm.querySelectorAll('.alert')[0];
    const dateBeginPrevValue = dateBeginPrev.textContent.split('.')[2] + '-' +
        dateBeginPrev.textContent.split('.')[1] + '-' + dateBeginPrev.textContent.split('.')[0];
    const dateEndPrev = currentForm.querySelectorAll('.alert')[1];
    const dateEndPrevValue = dateEndPrev.textContent.split('.')[2] + '-' +
        dateEndPrev.textContent.split('.')[1] + '-' + dateEndPrev.textContent.split('.')[0];
    const formData = new FormData(this);
    fetch(this.action, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (dateBeginPrevValue > data.period_begin) {
                dateBeginPrev.textContent = data.period_begin;
            }
            if (dateEndPrevValue < data.period_end) {
                dateEndPrev.textContent = data.period_end;
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
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
            const currentDate = new Date()
            resultElement.textContent = `${currentDate.getHours()}:${currentDate.getMinutes()} — ${data.result} записей импортировано`;
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
});
