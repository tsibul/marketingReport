'use strict'

import {fillFormNode} from "./fillFormNode.js";

/**
 * Create form for edit from row
 * @param obj clickable row
 */
export async function createEditForm(obj) {
    const nodeElements = obj.childNodes;
    const objClasses = obj.classList;
    const newNode = document.createElement('form'); // block for new row
    newNode.classList.add('form-row');
    objClasses.forEach(function (el) {
        if (el !== 'dict-block__row') {
            newNode.classList.add(el);
        }
    });
    newNode.id = 'form-dict';
    await fillFormNode(obj, newNode, nodeElements);
}