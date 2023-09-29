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

document.addEventListener('mousedown', function (element) {
    try {
        if (element.target !== document.querySelector('form').parentElement &&
            !document.querySelector('form').parentElement.contains(element.target)) {
            const buttonClose = document.querySelector('form').querySelector('.btn-close');
            cancelEditDictionary(buttonClose);
        }
    } catch (exception) {
    }
});

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
    const parentObj = obj.parentElement.parentElement;
    const row = parentObj.parentElement;
    parentObj.remove();
    const elementId = row.dataset.id;
    if (elementId === '') {
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
    const updateForm = obj.parentElement.parentElement;
    const dictionaryType = updateForm.parentElement.id.split('-')[0];
    const fetchPath = '/marketing/dict_update/' + dictList[dictionaryType];
    const formData = new FormData(updateForm);
    fetch(fetchPath, {
        method: 'POST',
        body: formData,
    })
        .then(async () => {
            const formFields = updateForm.querySelectorAll('[name]');
            const parentRow = updateForm.parentElement;
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
        })
        .catch((error) => {
            console.error(error);
        });
}

document.addEventListener('mouseover', async (event) =>  {
    const lastRecords = document.querySelectorAll('div[data-last]:not([data-last = ""])')
    const rowCurrent = event.target;
    for (const el of lastRecords) {
        if (el.contains(rowCurrent)) {
            const dictType = dictList[rowCurrent.id.split('-')[0]];
            const jsonUrl = `json_dict_next_20/${rowCurrent.dataset.last}/${dictType}`
            const [nextRecords] = await fetchJsonData(jsonUrl);
            alert(dictType)
        }
    }
});