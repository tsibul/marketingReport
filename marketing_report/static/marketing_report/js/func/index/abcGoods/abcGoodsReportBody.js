'use strict'

import {createPeriodRow} from "../createPeriodRow.js";
import {toggleDisplay} from "../abc/abcReportBody.js";

export function abcGoodsReportBody(report) {
    const body = document.createElement('div');
    body.appendChild(createGoodsParameterRow());
    const perData = createPeriodRow(report);

    const periodData = perData[0];
    const gridClass = perData[1];
    const periodRow = perData[2];
    body.appendChild(periodRow)

    report.report.report_data.items.forEach(group => {

        fillPeriodRow(body, gridClass, periodData, group, 0);
    });
    return body;
}

function createGoodsParameterRow() {
    const parameterRow = document.createElement('div');
    parameterRow.classList.add('abc', 'abc__parameter-row');
    const timeNow = Date.now();
    const parameterRowHTML = `
    <p>параметр:</p>
    <span>
        <input type="checkbox" id="sales-vat-${timeNow}" class="sales-vat-check" checked>
        <label for="sales-vat-${timeNow}">продажи без НДС</label>
    </span>
    <span>
        <input type="checkbox" id="quantity-${timeNow}" class="quantity-check">
        <label for="quantity-${timeNow}">количество единиц</label>
    </span>
    <span>
        <input type="checkbox" id="no-sales-${timeNow}" class="no-sales-check">
        <label for="no-sales-${timeNow}">количество продаж</label>
    </span>
    <span>
        <input type="checkbox" id="price-${timeNow}" class="price-check">
        <label for="price-${timeNow}">средняя цена</label>
    </span>
    <span>
        <input type="checkbox" id="average-quantity-${timeNow}" class="average-quantity-check">
        <label for="average-quantity-${timeNow}">среднее количество</label>
    </span>
    <span>
        <input type="checkbox" id="min-quantity-${timeNow}" class="min-quantity-check">
        <label for="min-quantity${timeNow}">минимальное количество</label>
    </span>
    `;
    parameterRow.insertAdjacentHTML('afterbegin', parameterRowHTML);
    let section;
    section = parameterRow.closest('section');
    parameterRow.querySelector('.sales-vat-check').addEventListener('change', (e) => {
        section = parameterRow.closest('section');
        section.querySelectorAll('.sales-vat').forEach(element => toggleDisplay(element, e.target));
    });
    parameterRow.querySelector('.quantity-check').addEventListener('change', (e) => {
        section = parameterRow.closest('section');
        section.querySelectorAll('.quantity').forEach(element => toggleDisplay(element, e.target));
    });
    parameterRow.querySelector('.no-sales-check').addEventListener('change', (e) => {
        section = parameterRow.closest('section');
        section.querySelectorAll('.no-sales').forEach(element => toggleDisplay(element, e.target));
    });
    parameterRow.querySelector('.price-check').addEventListener('change', (e) => {
        section = parameterRow.closest('section');
        section.querySelectorAll('.price').forEach(element => toggleDisplay(element, e.target));
    });
    parameterRow.querySelector('.average-quantity-check').addEventListener('change', (e) => {
        section = parameterRow.closest('section');
        section.querySelectorAll('.average-quantity').forEach(element => toggleDisplay(element, e.target));
    });
    parameterRow.querySelector('.min-quantity-check').addEventListener('change', (e) => {
        section = parameterRow.closest('section');
        section.querySelectorAll('.min-quantity').forEach(element => toggleDisplay(element, e.target));
    });
    return parameterRow;
}

// export function toggleDisplay(element, check) {
//     if (check.checked) {
//         element.style.display = 'block';
//     } else {
//         element.style.display = 'none';
//     }
//
// }


function fillPeriodRow(body, gridClass, periodData, group, margin) {
    const rowDetails = document.createElement('details');
    const row = document.createElement('summary');
    row.classList.add('abc', gridClass, 'abc__summary', 'margin__'+ margin);
    rowDetails.appendChild(row);
    let unitTitle;
    unitTitle = group.name;
    row.insertAdjacentHTML('afterbegin',
        `<div>${unitTitle}</div>
          <div class="abc__params">
            <div class="sales-vat small-font">продажи (тыс. руб.)</div>
            <div class="quantity small-font" >кол-во шт.</div>
            <div class="no-sales small-font">кол-во продаж</div>
            <div class="price small-font">средняя цена</div>
            <div class="average-quantity small-font">ср. кол-во шт</div>
            <div class="min-quantity small-font">мин. кол-во</div>
          </div>`);
    periodData.forEach(per => {
        const periodItem = document.createElement('div');
        periodItem.classList.add('abc__params');
        group.periods.forEach(detail => {
            if (detail.period__name === per.name) {
                periodItem.insertAdjacentHTML("beforeend",
                    `
            <div class="abc__digit sales-vat">${detail.goods_total_sales}</div>
            <div class="abc__digit quantity">${detail.goods_total_quantity}</div>
            <div class="abc__digit no-sales">${detail.goods_total_no_sales}</div>
            <div class="abc__digit price">${detail.goods_average_price}</div>        
            <div class="abc__digit average-quantity">${detail.goods_average_sales_quantity}</div>        
            <div class="abc__digit min-quantity">${detail.goods_minimal_quantity}</div>        
                `);
            }
            row.appendChild(periodItem);
        });
    });
    row.insertAdjacentHTML('beforeend',
        `
    <div class="abc__params">
        <div class="abc__digit sales-vat">${group.totals.goods_total_sales}</div>
        <div class="abc__digit quantity">${group.totals.goods_total_quantity}</div>
        <div class="abc__digit no-sales">${group.totals.goods_total_no_sales}</div>
        <div class="abc__digit price">${group.totals.goods_average_price}</div>        
        <div class="abc__digit average-quantity">${group.totals.goods_average_sales_quantity}</div>        
        <div class="abc__digit min-quantity">${group.totals.goods_minimal_quantity}</div>
    </div>        
    `);
    body.appendChild(rowDetails);
    const marginCurrent = margin + 1;
    if (typeof group.items !== 'undefined') {
        group.items.forEach(item => fillPeriodRow(rowDetails, gridClass, periodData, item, marginCurrent))
    }
}