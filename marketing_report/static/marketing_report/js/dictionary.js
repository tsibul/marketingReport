const dictList = {
    matrix: 'GoodMatrixType',
    crm: 'GoodCrmType',
    printType: 'PrintType',
    colorScheme: 'ColorScheme',
    color: 'Color',
    customer: 'Customer',
    customerTypes: 'CustomerTypes',
    customerGroups: 'CustomerGroups',
    goods: 'goods',
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
    objClasses.forEach(function (el){
       if(el !== 'dict-section-block-row') {
           newNode.classList.add(el);
       }
    });
    newNode.id = 'form-dict';
    let childNode;
    let changes = 0;
    nodeElements.forEach(function (node) {
        if (node.tagName === 'DIV' && !node.hidden) {
            childNode = document.createElement('input'); // block for input
            childNode.classList.add('form-input', 'dict-section-block-text', 'dict__form-input');
            childNode.type = 'text';
            if(node.dataset.name != null){
            childNode.name = node.dataset.name;} else {
                childNode.readOnly = true;
                childNode.classList.add('form-input__inactive');
            }
            childNode.setAttribute('value', node.textContent);
            newNode.appendChild(childNode)
            changes += 1;
        }
        node.hidden = true;
    });
    if (changes === 0) {
        return
    }
    obj.querySelector('.id-hidden').setAttribute('form', 'form-dict')
    newNode.appendChild(createButtonBlock());
    obj.appendChild(newNode);
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
    buttonBlock.classList.add('dict__btn-block'); // block for buttons submit & cancel
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
            let fieldList;
        })
        .catch((error) => {
            console.error(error);
        });
}