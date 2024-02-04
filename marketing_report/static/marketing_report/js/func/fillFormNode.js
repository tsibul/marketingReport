'use strict'

import {createButtonBlock} from "./createButtonBlock.js";
import {dictList} from "../const/dictList.js";
import {dropdownCode} from "./dropdown/dropdownCode.js";
import {booleanDropdown} from "./dropdown/booleanDropdown.js";
import {fetchJsonData} from "./fetchJsonData.js";
import {fillLines} from "./dropdown/fillLines.js";
import {filterList} from "./dropdown/filterList.js";
import {stringToDateTime} from "./stringToDateTime.js";
import {selectFromList} from "./dropdown/selectFromList.js";
import {dropdownListenerHide} from "./dropdown/dropdownListenerHide.js";
import {dropDownListenerVisible} from "./dropdown/dropDownListenerVisible.js";

/**
 * Fill editable form-row from row
 * @foreign-key marker for create dropdown input
 * @bool-field marker for create boolean dropdown
 * @changes number of inputs created in form, if '0' form doesn't create
 * @param obj row to edit
 * @param newNode new form row for edit
 * @param nodeElements nodeList of elements of initial row
 * @returns {Promise<void>}
 */
export async function fillFormNode(obj, newNode, nodeElements) {
    let changes = 0;
    for (const node of nodeElements) {
        if (node.tagName === 'DIV' && !node.hidden) {
            if (node.classList.contains('foreign-key')) {
                await createDropdown(node);
            } else if (node.classList.contains('bool-field')) {
                await createBoolean(node);
            } else {
                await createInput(node);
            }
        }
        node.hidden = true;
    }
    if (changes === 0) {
        return
    }
    if (obj.querySelector('.id-hidden')) {
        obj.querySelector('.id-hidden').setAttribute('form', 'form-dict');
    }
    newNode.appendChild(createButtonBlock());
    obj.appendChild(newNode);

    /**
     * Create input field from initial field
     * @data.name marker if the field is editable if data.name is null input will be inactive
     * @date-field marker for datetime field — to convert to db format
     * @param node initial element to convert to input
     * @returns {Promise<void>}
     */
    async function createInput(node) {
        let childInputNode;
        childInputNode = document.createElement('input'); // block for input
        childInputNode.classList.add('form-input', 'dict-block__text', 'dict__form-input');
        if (node.dataset.name != null) {
            childInputNode.name = node.dataset.name;
        } else {
            childInputNode.readOnly = true;
            childInputNode.classList.add('form-input__inactive');
        }
        if (node.classList.contains('date-field')) {
            childInputNode.type = 'datetime-local';
            childInputNode.value = stringToDateTime(node.textContent);
        } else {
            childInputNode.type = 'text';
            childInputNode.setAttribute('value', node.textContent);
        }
        newNode.appendChild(childInputNode)
        changes += 1;
    }

    /**
     * Create dropdown input field from initial field (marker class 'foreign-key')
     * @dataset.filter marker that this dropdown affected on some other field
     * in this case forms filtered dropdown
     * @childDropDownNode - dropdown html template
     * @param node initial element to convert to dropdown input
     * @returns {Promise<void>}
     */
    async function createDropdown(node) {
        let childDropdownNode;
        const parentRow = node.closest('.dict-block__row');
        const dictType = dictList[node.dataset.name];
        childDropdownNode = document.createElement('div');
        childDropdownNode.insertAdjacentHTML('beforeend', dropdownCode);
        childDropdownNode.querySelector('.dropdown__input').addEventListener('keyup', e => {
            filterList(e.target);
        });
        childDropdownNode = childDropdownNode.firstElementChild;
        childDropdownNode.addEventListener('click', e => {
            dropdownListenerHide(childDropdownNode, e);
        });
        childDropdownNode.addEventListener('click', e =>{
            dropDownListenerVisible(childDropdownNode, e);
        });
        childDropdownNode.querySelector('.dropdown__hidden').name = node.dataset.name;
        const filterModel = dictList[node.dataset.filter];
        const ulContent = childDropdownNode.querySelector('.dropdown__content');
        let jsonUrl;
        if (filterModel && parentRow.dataset.id !== 'e') {
            const filterNo = parentRow.querySelector(`[data-name = "${node.dataset.filter}"]`).dataset.id;
            jsonUrl = `/marketing/dictionary_json_filter/${dictType}/${filterModel}/${Number.parseInt(filterNo)}`;
            childDropdownNode.querySelector('.dropdown__hidden').dataset.filter = node.dataset.filter;
        } else if (!filterModel) {
            jsonUrl = `/marketing/dictionary_json_filter/${dictType}/default/0`;
        } else {
            childDropdownNode.querySelector('.dropdown__hidden').dataset.filter = node.dataset.filter;
            jsonUrl = `/marketing/dictionary_json_filter/default/default/0`;
        }
        const jsonData = await fetchJsonData(jsonUrl);
        const dictionaryList = JSON.parse(jsonData);
        if (!dictionaryList) {
            childDropdownNode.querySelector('.dropdown__hidden').value = Object.keys(dictionaryList[0])[0];
            childDropdownNode.querySelector('.dropdown__input_dict').value = Object.values(dictionaryList[0])[0];
            childDropdownNode.querySelector('.dropdown__input_dict').dataset.value = Object.values(dictionaryList[0])[0];
        }
        fillLines(ulContent, dictionaryList);
        fillFields(node, childDropdownNode);
    }

    /**
     * Create boolean dropdown input field from initial field (marker class 'bool-field')
     * @param node initial element to convert to boolean dropdown
     * @returns {Promise<void>}
     */
    async function createBoolean(node) {
        let childBooleanNode
        childBooleanNode = document.createElement('div');
        childBooleanNode.insertAdjacentHTML('beforeend', booleanDropdown);
        childBooleanNode = childBooleanNode.firstElementChild;
        childBooleanNode.querySelectorAll('li').forEach(line => {
            line.addEventListener('click', e => {
                e.stopPropagation();
                selectFromList(e.target);
            });
        });
        childBooleanNode.querySelector('.dropdown__hidden').name = node.dataset.name;
        childBooleanNode.addEventListener('click', e =>{
            dropDownListenerVisible(childBooleanNode, e);
        });
        fillFields(node, childBooleanNode);
    }

    /**
     * fill inputs with initial value in case of editing row then append it to form
     * @param node initial element to convert to form input
     * @param childResNode created input element which should be appended to form
     */
    function fillFields(node, childResNode) {
        childResNode.querySelector('.dropdown__input').value = node.textContent.replace(/\s+/g, ' ');
        childResNode.querySelector('.dropdown__input').dataset.value = node.textContent.replace(/\s+/g, ' ');
        childResNode.querySelector('.dropdown__hidden').value = node.dataset.id;
        newNode.appendChild(childResNode);
        changes += 1;
    }
}
