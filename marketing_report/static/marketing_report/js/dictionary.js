const dictList = {
    matrix: 'GoodMatrixType',
    crm: 'GoodCrmType',
    printType: 'PrintType',
    colorScheme: 'ColorScheme',
    color: 'Color',
    customer: 'Customer',
    customerType: 'CustomerTypes',
    customerGroup: 'CustomerGroups',
    goods: 'Goods',
};
const addButtons = document.querySelectorAll('.btn_add');
const searchButtons = document.querySelectorAll('.search_submit');
const searchCloseButtons = document.querySelectorAll('.search_clear');
const deleteButtons = document.getElementsByClassName('.btn_delete');

window.onload = function () {
    const summary = document.querySelectorAll('.dict-block__header_block-space');
    const fn = function (e) {
        if (e.keyCode === 32) {
            e.preventDefault();
        }
    };
    summary.forEach(el => {
        el.onkeyup = fn;
    });
};
function typeDict(row) {
    return dictList[row.id.split('-')[0]];
}
function editDictionary(obj) {
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
    fillFormNode();

    function fillFormNode() {
        let childNode;
        let changes = 0;
        nodeElements.forEach(function (node) {
            if (node.tagName === 'DIV' && !node.hidden) {
                if (node.classList.contains('foreign-key')) {
                    createDropdown(node);
                } else if (node.classList.contains('bool-field')) {
                    createBoolean(node);
                } else {
                    createInput(node);
                }
            }
            node.hidden = true;
        });
        if (changes === 0) {
            return
        }
        obj.querySelector('.id-hidden').setAttribute('form', 'form-dict')
        newNode.appendChild(createButtonBlock());
        obj.appendChild(newNode);

        function createInput(node) {
            childNode = document.createElement('input'); // block for input
            childNode.classList.add('form-input', 'dict-block__text', 'dict__form-input');
            childNode.type = 'text';
            if (node.dataset.name != null) {
                childNode.name = node.dataset.name;
            } else {
                childNode.readOnly = true;
                childNode.classList.add('form-input__inactive');
            }
            childNode.setAttribute('value', node.textContent);
            newNode.appendChild(childNode)
            changes += 1;
        }

        function createDropdown(node) {
            childNode = document.getElementById(node.dataset.name).querySelector('div').cloneNode(true);
            fillFields(node, childNode);
        }

        function createBoolean(node) {
            childNode = document.getElementById('boolean').querySelector('div').cloneNode(true);
            childNode.querySelector('.dropdown__hidden').name = node.dataset.name;
            fillFields(node, childNode);
        }

        function fillFields(node, childNode) {
            childNode.querySelector('.dropdown__input').value = node.textContent.replace(/\s+/g, ' ');
            childNode.querySelector('.dropdown__input').dataset.value = node.textContent.replace(/\s+/g, ' ');
            childNode.querySelector('.dropdown__hidden').value = node.dataset.id;
            newNode.appendChild(childNode);
            changes += 1;
        }
    }
}
function cancelEditDictionary(obj) {
    const parentObj = obj.closest('.form-row');
    const row = obj.closest('.dict-block__row');
    parentObj.remove();
    const elementId = row.dataset.id;
    if (elementId === 'e') {
        row.remove();
        return;
    }
    row.childNodes.forEach(function (element) {
        if (element.hidden) {
            element.hidden = false
        }
    });
    row.querySelector('.id-hidden').setAttribute('form', '');
}
function createButtonBlock() {
    /* create button block for buttons submit & cancel */
    let childNode;
    const buttonBlock = document.createElement('div');
    buttonBlock.classList.add('dict__button-block', 'button-block'); // block for buttons submit & cancel
    childNode = document.createElement('button'); //button cancel
    childNode.innerHTML = '<i class="fa fa-solid fa-xmark" ></i>';
    childNode.classList.add('btn', 'btn-close', 'dict__btn');
    childNode.setAttribute('onclick', 'event.stopPropagation(); cancelEditDictionary(this);');
    childNode.type = 'button';
    buttonBlock.appendChild(childNode);
    childNode = document.createElement('button'); // button submit
    childNode.innerHTML = '<i class="fa fa-solid fa-check"></i>';
    childNode.classList.add('btn', 'btn-save', 'dict__btn');
    childNode.setAttribute('onclick', 'event.stopPropagation(); saveDictionaryRecord(this);');
    childNode.type = 'submit';
    buttonBlock.appendChild(childNode);
    return buttonBlock;
}
function saveDictionaryRecord(obj) {
    event.preventDefault();
    const updateForm = obj.closest('.form-row');
    const dictionaryType = updateForm.parentElement.id.split('-')[0];
    const fetchPath = '/marketing/dict_update/' + dictList[dictionaryType];
    const formData = new FormData(updateForm);
    fetch(fetchPath, {
        method: 'POST',
        body: formData,
    })
        .then(async () => {
            const formFields = updateForm.querySelectorAll('[name]');
            const parentRow = updateForm.closest('.dict-block__row');
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
async function appendNewRows(rowCurrent, blockContent, searchString) {
    let newRow;
    const rowCopy = blockContent.querySelector('.dict-block__row_hidden');
    const dictType = typeDict(rowCurrent);
    const jsonUrl = `/marketing/json_dict_next_20/${dictType}/${rowCurrent.dataset.last}/default/${searchString}`;
    const jsonData = await fetchJsonData(jsonUrl);
    const nextRecords = JSON.parse(jsonData);
    let i = 0;
    nextRecords.forEach((record) => {
        i++;
        newRow = rowCopy.cloneNode(true);
        fillNewRow(record, i, newRow);
        newRow.classList.remove('dict-block__row_hidden');
        if (i === 20) {
            newRow.dataset.last = Number.parseInt(rowCurrent.dataset.last) + 20;
        }
        blockContent.appendChild(newRow);
    });
    rowCurrent.dataset.last = '';
}
async function fillNewRow(record, i, newRow) {
    const newRowElements = newRow.querySelectorAll('div[data-field]:not([data-field = ""])')
    newRow.dataset.id = record['pk'];
    newRow.id = newRow.id.slice(0, -1) + record['pk'];
    newRow.querySelector('.id-hidden').value = record['pk'];
    for (const rowElement of newRowElements) {
        let fieldName = rowElement.dataset.field;
        if (rowElement.classList.contains('foreign-key')) {
            rowElement.dataset.id = record.fields[fieldName];
            if (fieldName === 'customer_group') {
                if (record.fields[fieldName] !== null) {
                    let groupUrl = `/marketing/customer_group_json`;
                    let groupData = await fetchJsonData(groupUrl);
                    let customerGroups = JSON.parse(groupData);
                    let groupElement = customerGroups.filter((el) => {
                        return el['pk'] === record.fields[fieldName]
                    });
                    rowElement.textContent = groupElement[0].fields['group_name'];
                }
            } else {
                let foreignKeyElement;
                if (fieldName !== 'customer_type') {
                    foreignKeyElement = document.getElementById(fieldName);
                } else {
                    foreignKeyElement = document.getElementById('group_type');
                }
                let foreignKeyLi = foreignKeyElement
                    .querySelector(`[data-value = "${record.fields[fieldName]}"]`);
                rowElement.textContent = foreignKeyLi.textContent;
            }
        } else if (rowElement.classList.contains('bool-field')) {
            rowElement.textContent = record.fields[fieldName] ? 'Да' : 'Нет';
            rowElement.dataset.id = record.fields[fieldName] ? '1' : '0';
        } else {
            rowElement.textContent = record.fields[fieldName];
        }
    }
}
// Cancel Edit Dictionary
addEventListener('mousedown', function (element) {
    try {
        const parentRow = document.querySelector('form').closest('.dict-block__row')
        if (element.target !== parentRow && !parentRow.contains(element.target)) {
            const buttonClose = document.querySelector('form').querySelector('.btn-close');
            cancelEditDictionary(buttonClose);
        }
    } catch (exception) {
    }
});
// next 20 records
addEventListener('mouseover', async (event) => {
    const lastRecords = document.querySelectorAll('div[data-last]:not([data-last = ""])')
    const rowCurrent = event.target;
    const blockContent = rowCurrent.closest('.dict-block__content');
    let searchString = rowCurrent.closest('.dict-block').querySelector('.dict-block__form-input').value;
    if (searchString === '') {
        searchString = 'default';
    }
    // let newRow;
    for (const el of lastRecords) {
        if (el.contains(rowCurrent)) {
            await appendNewRows(rowCurrent, blockContent, searchString);
            // const rowCopy = blockContent.querySelector('.dict-block__row_hidden');
            // const dictType = typeDict(rowCurrent);
            // const jsonUrl = `/marketing/json_dict_next_20/${dictType}/${rowCurrent.dataset.last}/default/${searchString}`;
            // const jsonData = await fetchJsonData(jsonUrl);
            // const nextRecords = JSON.parse(jsonData);
            // let i = 0;
            // nextRecords.forEach((record) => {
            //     i++;
            //     newRow = rowCopy.cloneNode(true);
            //     fillNewRow(record, i, newRow);
            //     newRow.classList.remove('dict-block__row_hidden');
            //     if (i === 20) {
            //         newRow.dataset.last = Number.parseInt(rowCurrent.dataset.last) + 20;
            //     }
            //     blockContent.appendChild(newRow);
            // });
            // rowCurrent.dataset.last = '';
        }
    }
});
// Edit dictionary
addEventListener('mousedown', (event) => {
    addButtons.forEach((btn) => {
        if (event.target === btn) {
            const dictBlock = btn.closest('.dict-block');
            const blockContent = dictBlock.querySelector('.dict-block__content')
            const copyRow = dictBlock.querySelector('.dict-block__row_hidden');
            const newRow = copyRow.cloneNode(true);
            newRow.id = newRow.id.slice(0, -1) + 'e';
            newRow.dataset.id = 'e';
            copyRow.after(newRow);
            newRow.classList.remove('dict-block__row_hidden');
            editDictionary(newRow);
        }
    });
});
// new Record
addEventListener('mousedown', async event => {
    for (const btn of deleteButtons) {
        if (event.target === btn) {
            const row = event.target.closest('.dict-block__row');
            const idNo = row.dataset.id;
            const dictType = typeDict(row);
            row.remove();
            const url = `/marketing/dict_delete/${dictType}/${idNo}`;
            await fetch(url);
        }
    }
});
// Search
addEventListener('mousedown', async (search) => {
    for (const btn of searchButtons) {
        if (search.target === btn) {
            const dictBlock = search.target.closest('.dict-block');
            const searchString = dictBlock.querySelector('.dict-block__form-input').value;
            let searchValue;
            if (searchString === '') {
                searchValue = 'default';
            } else {
                searchValue = searchString.replaceAll(/  +/g, ' ').replaceAll(' ', '_')
            }
            const dictBlockContent = dictBlock.querySelector('.dict-block__content');
            const hiddenRow = dictBlockContent.querySelector('.dict-block__row_hidden');
            // const dictType = typeDict(hiddenRow);
            const temporaryRow = hiddenRow.cloneNode(true)
            temporaryRow.setAttribute('data-last', '0');
            dictBlockContent.appendChild(temporaryRow);
            dictBlockContent.innerHTML = '';
            dictBlockContent.appendChild(hiddenRow);
            await appendNewRows(temporaryRow, dictBlockContent, searchValue);
            temporaryRow.remove();
        }
    }
});

