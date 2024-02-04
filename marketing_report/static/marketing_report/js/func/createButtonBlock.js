'use strict'

import {cancelEditRecord} from "./cancelEditRecord.js";
import {saveDictionaryRecord} from "./saveDictionaryRecord.js";

/**
 * Create button block button block for buttons submit & cancel to the end of form
 * @returns {HTMLDivElement}
 */
export function createButtonBlock() {
    let childNode;
    const buttonBlock = document.createElement('div');
    buttonBlock.classList.add('dict__button-block', 'button-block'); // block for buttons submit & cancel
    childNode = document.createElement('button'); //button cancel
    childNode.innerHTML = '<i class="fa fa-solid fa-xmark" ></i>';
    childNode.classList.add('btn', 'btn-close', 'dict__btn');
    childNode.addEventListener('click', e =>{
        e.stopPropagation();
        cancelEditRecord(e.target);
    });
    childNode.type = 'button';
    buttonBlock.appendChild(childNode);
    childNode = document.createElement('button'); // button submit
    childNode.innerHTML = '<i class="fa fa-solid fa-check"></i>';
    childNode.classList.add('btn', 'btn-save', 'dict__btn');
    childNode.addEventListener('click', e =>{
        e.stopPropagation();
        saveDictionaryRecord(e.target);
    });
    childNode.type = 'submit';
    buttonBlock.appendChild(childNode);
    return buttonBlock;
}
