'use strict'

import {fetchJsonData} from "../fetchJsonData.js";

export async function importCustomers(btn, url) {
    btn.disabled = true;
    btn.classList.add('form-input__inactive');
    const counts = await fetchJsonData('/marketing/' + url);
    const newCustomers = btn.previousElementSibling;
    newCustomers.textContent = `импортировано ${counts.result}`;
    btn.disabled = false;
    btn.classList.remove('form-input__inactive');
}
