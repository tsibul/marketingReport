'use strict'

import {importFileModalClose} from "./func/import/importFileModalClose.js";
import {importFileModal} from "./func/import/importFileModal.js";
import {importCustomers} from "./func/import/importCustomers.js";
import {editTemporaryBase} from "./func/import/editTemporaryBase.js";
import {reassignPeriods} from "./func/import/reassignPeriods.js";

const buttonClose = document.querySelector('.modal.close');
const importModal = document.querySelector('#import-file-modal');

document.querySelector('#result').nextElementSibling
    .addEventListener('click', e => importFileModal(e.target, 'customers'));
document.querySelector('#resultSales').nextElementSibling
    .addEventListener('click', e => importFileModal(e.target, 'sales'));

document.querySelector('#updated-customers').nextElementSibling
    .addEventListener('click', e => editTemporaryBase(e.target));

document.querySelector('#import_new_customers').nextElementSibling
    .addEventListener('click', e => importCustomers(e.target, 'import_new_customers'));

document.querySelector('#import_changed_customers').nextElementSibling
    .addEventListener('click', e => importCustomers(e.target, 'import_changed_customers'));

document.querySelector('#period-end').nextElementSibling
    .addEventListener('click', e => reassignPeriods(e.target));

importModal.querySelector('.btn-close')
    .addEventListener('click', e => importFileModalClose(e.target));

// importModal.querySelector('.btn-save')
//     .addEventListener('click', e => importFileModal(e.target, 'sales'));


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
            const btnDisabled = document.querySelector('.form-input__inactive');
            btnDisabled.disabled = false;
            btnDisabled.classList.remove('form-input__inactive');
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
});
