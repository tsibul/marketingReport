'use strict'

export function dropDownListenerVisible(dropdown, element) {
    if (dropdown.contains(element.target)) {
        dropdown.querySelector('ul').classList.add('visible');
    }
}