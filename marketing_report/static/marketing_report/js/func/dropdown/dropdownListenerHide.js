'use strict'

export function dropdownListenerHide(dropdown) {
    let obj;
    if (dropdown.querySelector('ul').classList.contains('visible')) {
        obj = dropdown;
    }
    if (obj != null && !obj.contains(dropdown)) {
        obj.querySelector('ul').classList.remove('visible');
        obj.querySelector('.dropdown__input').value = obj.querySelector('.dropdown__input').dataset.value;
    }
}