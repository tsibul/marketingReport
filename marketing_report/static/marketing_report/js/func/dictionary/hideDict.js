'use strict'

export function hideDict(hiddenBlock, dictToCopy, dictHeader, dictDetails, element) {
    dictToCopy.open = false
    hiddenBlock.appendChild(dictToCopy);
    element.nextElementSibling.classList.remove('active');
    element.nextElementSibling.querySelector('i').classList.remove('fa-flip');
    let i = true
    dictDetails.querySelectorAll('input').forEach(item => {
        if (item.checked) {
            i = false;
        }
    });
    if (i) {
        dictHeader.classList.remove('active');
    }
}