// parse json on main page
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