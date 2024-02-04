'use strict'

import {typeDict} from "./typeDict.js";
import {fetchJsonData} from "./fetchJsonData.js";

/**
 * Updates db from update form (looks like rows of inputs)
 * @param updateForm — form to save in DB
 * @param fetchPath — path to url of (dictionary_update in dictionary.py)
 */
export function saveEditForm(updateForm, fetchPath) {
    const formFields = updateForm.querySelectorAll('[name]');
    const parentRow = updateForm.closest('.dict-block__row');
    const quantityField = updateForm.querySelector(`[name = "quantity"]`);
    if (quantityField && (!quantityField.value || quantityField.value === '0')) {
        updateForm.remove();
        if (parentRow.dataset.id !== 'e') {
            parentRow.childNodes.forEach(function (element) {
                if (element.hidden) {
                    element.hidden = false
                }
            });
        } else {
            parentRow.remove();
        }
    } else {
        const formData = new FormData(updateForm);
        fetch(fetchPath, {
            method: 'POST',
            body: formData,
        })
            .then(async () => {
                formFields.forEach((field) => {
                    if (!field.classList.contains('dropdown__hidden')) {
                        parentRow.querySelector(`[data-name = ${field.name}]`).textContent = field.value;
                    } else {
                        parentRow.querySelector(`[data-name = ${field.name}]`).textContent =
                            field.parentElement.querySelector('.dropdown__input').value;
                    }
                });
                updateForm.remove();
                parentRow.childNodes.forEach(function (element) {
                    if (element.hidden) {
                        element.hidden = false
                    }
                });
                parentRow.querySelector('.id-hidden').setAttribute('form', '');
                if (parentRow.dataset.id === 'e') {
                    const dictType = typeDict(parentRow);
                    const jsonUrl = `/marketing/dictionary_last_id/${dictType}`;
                    const jsonData = await fetchJsonData(jsonUrl);
                    const idRecord = JSON.parse(jsonData)['id__max'];
                    parentRow.dataset.id = idRecord;
                    parentRow.querySelector('.id-hidden').value = idRecord;
                    parentRow.id = parentRow.id.split('-')[0] + '-' + idRecord;
                }
            })
            .catch((error) => {
                console.error(error);
            });
    }
}
