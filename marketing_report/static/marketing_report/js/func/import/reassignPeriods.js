'use strict'

export function reassignPeriods(button) {
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