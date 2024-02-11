'use strict'

import {fetchJsonData} from "../fetchJsonData.js";

export async function customerFirstLastDate(btn) {
    btn.disabled = true;
    btn.classList.add('form-input__inactive');
    await fetch('/marketing/first_last_sales_dates');
    btn.previousElementSibling.textContent = 'выполнено';
    btn.disabled = false;
    btn.classList.remove('form-input__inactive');
    // .then(response => {})
    // .then(() => {
    //     btn.previousElementSibling.textContent = 'выполнено';
    //     btn.disabled = false;
    //     btn.classList.remove('form-input__inactive');
    // });
}