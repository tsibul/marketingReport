'use strict'
// parse json on main page
export function periodsList() {
    return JSON.parse(document.getElementById('periods').textContent);
}

export function customerReports() {
    return JSON.parse(document.getElementById('json-cst-reports').textContent);
}

export function goodsReports() {
    return JSON.parse(document.getElementById('json-goods-reports').textContent);
}

export function moneyArguments() {
    return JSON.parse(document.getElementById('json-money-arguments').textContent);
}

export function timeArguments() {
    return JSON.parse(document.getElementById('json-time-arguments').textContent);
}