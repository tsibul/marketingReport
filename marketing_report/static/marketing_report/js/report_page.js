import {selectFromList} from "./func/dropdown/selectFromList.js";
import {periodsList, goodsReports, customerReports, timeArguments, moneyArguments} from "./func/reports.js";

async function selectFromListMod(obj) {
    const parentObj = obj.parentElement.parentElement;
    const valuePrevious = parentObj.querySelector('.dropdown__hidden').value;
    const valueCurrent = obj.dataset.value;
    await selectFromList(obj);
    const moneyReports = document.querySelector('#money-reports').value.split(',');
    const paramContent = parentObj.parentElement.querySelector('[id^="parameter-select"]')
        .parentElement.querySelector('.dropdown__content');
    let newLines;
    if (moneyReports.includes(valuePrevious) && !moneyReports.includes(valueCurrent)) {
        newLines = document.querySelector('#time-arguments');
        paramContent.innerHTML = newLines.innerHTML;
        await selectFromList(paramContent.querySelector('li'))
    } else if (!moneyReports.includes(valuePrevious) && moneyReports.includes(valueCurrent)) {
        newLines = document.querySelector('#money-arguments');
        paramContent.innerHTML = newLines.innerHTML;
        await selectFromList(paramContent.querySelector('li'))
    }
}


// add report block
function newReport(thisObj, reportType) {
    const oldId = changeReportBlockId(thisObj);
    const tempNode = temporaryNode();
    thisObj.parentNode.insertBefore(tempNode, thisObj);
    setTimeout(function () {
        tempNode.style.width = '360px';
    }, 0);
    setTimeout(function () {
        tempNode.remove();
        const newNode = addReportBlock(reportType, oldId);
        newNode.classList.add('temp-width');
        thisObj.parentNode.insertBefore(newNode, thisObj);
        addPeriodList(newNode);
        addReportList(newNode, reportType);
    }, 300);


    function temporaryNode() {
        const tempNode = document.createElement('div')
        tempNode.id = 'temp-node';
        tempNode.className = 'temp-block';
        return tempNode;
    }

    function changeReportBlockId(thisObj) {
        // add 1 to id for block "add report"
        const oldId = thisObj.id.split('-').pop();
        const newId = (parseInt(oldId) + 1).toString();
        thisObj.id = thisObj.id.replace(oldId, newId);
        return oldId;
    }

    function addReportBlock(reportType, oldId) {
        // clone block from down change ids for all elements including connected labels
        const newNode = document.getElementById('report-' + reportType).cloneNode(true)
        newNode.id = 'report-' + oldId;
        newNode.querySelectorAll('[id$="' + reportType + '"]').forEach(function (element) {
            element.id = element.id.replace(reportType, oldId);
        });
        newNode.querySelectorAll('[for$="' + reportType + '"]').forEach(function (element) {
            element.setAttribute('for', element.getAttribute('for').replace(reportType, oldId));
        });
        newNode.classList.add('zero-width');
        return newNode;
    }

    function addPeriodList(newNode) {
        const periodSelect = newNode.querySelector('[id^="period-select"]')
            .parentElement.querySelector('.dropdown__content');
        let newOption;
        for (const [key, value] of Object.entries(periodsList())) {
            newOption = document.createElement('li');
            newOption.dataset.value = key;
            newOption.textContent = value;
            newOption.setAttribute('onclick', 'event.stopPropagation(); selectFromList(this);')
            periodSelect.appendChild(newOption);
        }
    }

    function addReportList(newNode, reportType) {
        const reportSelect = newNode.querySelector('[id^="report-select"]')
            .parentElement.querySelector('.dropdown__content');
        const reportArray = reportType === 0 ? customerReports() : goodsReports();
        let newOption;
        reportArray.forEach(function (report) {
            newOption = document.createElement('li');
            newOption.dataset.value = report['code'];
            newOption.textContent = report['description'];
            newOption.setAttribute('onclick', 'event.stopPropagation(); selectFromListMod(this);')
            reportSelect.appendChild(newOption);
        });
    }
}

// change argument list
function changeArgumentList(thisObj) {
    const parentObj = thisObj.parentElement;
    let newOptions;
    if (thisObj.value === 'MIG' || thisObj.value === 'CLR') {
        newOptions = timeArguments();
        parentObj.querySelector('[for^="parameter-select"]').textContent = 'время жизни';
    } else {
        newOptions = moneyArguments();
        parentObj.querySelector('[for^="parameter-select"]').textContent = 'показатель';
    }
    const argumentSelect = parentObj.querySelector('[id^="parameter-select"]');
    argumentSelect.replaceChildren();
    let newOption;
    newOptions.forEach(function (argument) {
        newOption = document.createElement('option');
        newOption.value = argument['code'];
        newOption.textContent = argument['description'];
        argumentSelect.appendChild(newOption);
    });
    parentObj.querySelector('[for^="parameter-select"]');
}

// remove report block
function reportRemove(thisObj) {
    const parentObj = thisObj.parentElement.parentElement;
    parentObj.innerHTML = '';
    parentObj.classList.add('report__remove');
    setTimeout(function () {
        parentObj.remove();
    }, 295)
}

// build report
function buildReport(thisObj) {
    const parentObj = thisObj.parentElement.parentElement;
    const blockId = parentObj.id.split('-').pop();
    const reportNo = parseInt(blockId) < 10000 ? '0' : '10000';
    const reportType = parentObj.querySelector('[id^="report-select"]').value;
    const reportTitle = reportNo === '0' ? 'Клиенты. ' + findReport(reportType, customerReports()) : 'Товары. ' + findReport(reportType, goodsReports());
    const period = parentObj.querySelector('[id^="period-select"]').value;
    const dates = parentObj.querySelectorAll('[type="date"]');
    const dateBegin = dates[0].value;
    const dateEnd = dates[1].value;
    const argument = parentObj.querySelector('[id^="parameter-select"]').value;
    if (dateBegin !== '' && dateEnd !== '' && dateBegin < dateEnd) {
        changeHeadingStyle();
        emptyReportBlockBig();
    } else if (dateBegin === '') {
        dates[0].focus();
    } else {
        dates[1].focus();
    }

    function findReport(reportType, array) {
        const element = array.find(function (el) {
            return el['code'] === reportType
        });
        return element['description']
    }

    function emptyReportBlockBig() {
        parentObj.classList.add('report-long');
        const reportHeading = parentObj.querySelector('.border-title')
        reportHeading.textContent = reportTitle;
        const dateRow = parentObj.querySelector('.date-row').cloneNode(true);
        const reportSelector = parentObj.querySelector('[id^="report-select"]').parentElement.cloneNode(true);
        reportSelector.value = parentObj.querySelector('[id^="report-select"]').value;
        reportSelector.style.display = 'none';
        const periodSelector = parentObj.querySelector('[id^="period-select"]').parentElement.cloneNode(true);
        periodSelector.value = parentObj.querySelector('[id^="period-select"]').value;
        periodSelector.classList.add('report-long_period');
        const argumentSelector = parentObj.querySelector('[id^="parameter-select"]').parentElement.cloneNode(true);
        argumentSelector.value = parentObj.querySelector('[id^="parameter-select"]').value;
        argumentSelector.classList.add('report-long_parameter');
        const periodText = document.createElement('label');
        periodText.textContent = ' детализация ';
        periodText.setAttribute('for', periodSelector.id);
        const argumentText = document.createElement('label');
        argumentText.textContent = ' показатель ';
        argumentText.setAttribute('for', argumentSelector.id);

        parentObj.querySelector('.report-block-content').innerHTML = '';
        parentObj.querySelector('.report-header').replaceChildren(reportHeading, dateRow, argumentText, argumentSelector, periodText, periodSelector, reportSelector);
    }

    function changeHeadingStyle() {
        parentObj.querySelector('.report-header').classList.add('report-long__header');
    }
}