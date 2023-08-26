
// add report block
function newReport(thisObj, reportType) {
    const oldId = changeReportBlockId(thisObj);
    const newNode = addReportBlock(reportType, oldId);
    thisObj.parentNode.insertBefore(newNode, thisObj);
    addPeriodList(newNode);
    addReportList(newNode, reportType);


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
        return newNode;
    }

    function addPeriodList(newNode) {
        const periodSelect = newNode.querySelector('[id^="period-select"]');
        let newOption;
        for (const [key, value] of Object.entries(periodsList())) {
            newOption = document.createElement('option');
            newOption.value = key;
            newOption.textContent = value;
            periodSelect.appendChild(newOption);
        }
    }

    function addReportList(newNode, reportType) {
        const periodSelect = newNode.querySelector('[id^="report-select"]');
        const reportArray = reportType === 0 ? customerReports() : goodsReports();
        let newOption;
        reportArray.forEach(function (report) {
            newOption = document.createElement('option');
            newOption.value = report['code'];
            newOption.textContent = report['description'];
            periodSelect.appendChild(newOption);
        });
    }
}

// change argument list
function changeArgumentList(thisObj){
    const parentObj = thisObj.parentElement;
    let newOptions;
    if(thisObj.value === 'MIG'){
        newOptions = timeArguments();
        parentObj.querySelector('[for^="parameter-select"]').textContent = 'время жизни';
    } else {
        newOptions = moneyArguments();
        parentObj.querySelector('[for^="parameter-select"]').textContent = 'показатель';
    }
    const argumentSelect = parentObj.querySelector('[id^="parameter-select"]');
    argumentSelect.replaceChildren();
    let newOption;
    newOptions.forEach(function (argument){
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
    parentObj.style.border = 'none';
    parentObj.style.padding = '0';
    parentObj.style.margin = '0';
    parentObj.style.minWidth = '0';
    parentObj.style.width = '0';
    setTimeout(function (){parentObj.remove();},295)
}

// build report
function buildReport(thisObj){
    const parentObj = thisObj.parentElement.parentElement;
    const blockId = parentObj.id.split('-').pop();
    const reportNo = parseInt(blockId) < 10000 ? '0' : '10000';
    const reportType = parentObj.querySelector('[id^="report-select"]').value;
    const period = parentObj.querySelector('[id^="period-select"]').value;
    const dates = parentObj.querySelectorAll('[type="date"]');
    const dateBegin = dates[0].value;
    const dateEnd = dates[1].value;
    const argument = parentObj.querySelector('[id^="parameter-select"]').value;
    if((dateBegin !== '') && (dateEnd !== '')){

    } else if(dateBegin === ''){
        dates[0].focus();
    } else {
        dates[1].focus();
    }
}