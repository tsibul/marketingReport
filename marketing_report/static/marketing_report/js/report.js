

// add report block
function newReport(thisObj, reportType) {
    const oldId = changeReportBlockId(thisObj);
    const newNode = addReportBlock(reportType, oldId);
    thisObj.parentNode.insertBefore(newNode, thisObj);
    addPeriodList(newNode);
    addReportList(newNode, reportType);
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
    return newNode;
}

function addPeriodList(newNode){
    const periodSelect = newNode.querySelector('[id^="period-select"]');
    let newOption;
    for (const [key, value] of Object.entries(periodsList())) {
        newOption = document.createElement('option');
        newOption.value = key;
        newOption.textContent = value;
        periodSelect.appendChild(newOption);
    }
}

function addReportList(newNode, reportType){
    const periodSelect = newNode.querySelector('[id^="report-select"]');
    const reportArray =  reportType === 0 ? customerReports() : goodsReports();
    let newOption;
     reportArray.forEach(function (report){
        newOption = document.createElement('option');
        newOption.value = report['code'];
        newOption.textContent = report['description'];
        periodSelect.appendChild(newOption);
    });
}

function changeArgumentList(){

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
//    thisObj.parentElement.parentElement.remove();
}

// parse json
function periodsList() {
    return JSON.parse(document.getElementById('periods').textContent);
}

function customerReports() {
    return JSON.parse(document.getElementById('json-cst-reports').textContent);
}

function goodsReports() {
    return JSON.parse(document.getElementById('json-goods-reports').textContent);
}

function moneyArguments() {
    return JSON.parse(document.getElementById('json-money-arguments').textContent);
}

function timeArguments() {
    return JSON.parse(document.getElementById('json-time-arguments').textContent);
}