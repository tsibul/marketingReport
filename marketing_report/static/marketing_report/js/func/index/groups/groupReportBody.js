'use strict'

import {createPeriodRow} from "../createPeriodRow.js";
import {createParameterRow} from "../abc/abcReportBody.js";

export function groupReportBody(report) {
    const body = document.createElement('div');
    body.appendChild(createParameterRow());
    const perData = createPeriodRow(report);

    const periodData = perData[0];
    const gridClass = perData[1];
    const periodRow = perData[2];
    body.appendChild(periodRow)

    let unitTitle;
    // unitTitle = document.createElement('div');
    // unitTitle.textContent = 'Всего';
    // unitTitle.classList.add('unit-title');
    // body.appendChild(unitTitle);

    report.report.report_data.forEach(unit => {
        unit.unitReport.forEach(group => {
            let groupDetail = document.createElement('details');
            let groupSummary = document.createElement('summary');
            groupSummary.classList.add('abc', gridClass, 'abc__summary');
            groupDetail.appendChild(groupSummary);
            if(group.group === 'T'){
                groupSummary.classList.add('unit-title');
                unitTitle = unit.unit;
            } else {
                unitTitle = 'Группа ' + group.group;
            }
            groupSummary.insertAdjacentHTML('afterbegin',
                `<div>${unitTitle}, Клиентов&nbsp;${group.customer_quantity}</div>
                  <div class="abc__params">
                    <div class="sales-vat">продажи с НДС</div>
                    <div class="sales">продажи без НДС</div>
                    <div class="profit">прибыль</div>
                    <div class="quantity">кол-во единиц (тыс.)</div>
                    <div class="no-sales">кол-во продаж</div>
                    <div class="average-check">средний чек</div>        
                  </div>`);
            periodData.forEach(per => {
                const periodItem = document.createElement('div');
                periodItem.classList.add('abc__params');
                group.group_details.forEach(detail => {
                    if (detail.period__name === per.name) {
                        periodItem.insertAdjacentHTML("beforeend",
                            `
                    <div class="abc__digit sales-vat">${detail.group_sales_with_vat}</div>
                    <div class="abc__digit sales">${detail.group_sales_without_vat}</div>
                    <div class="abc__digit profit">${detail.group_profit}</div>
                    <div class="abc__digit quantity">${detail.group_quantity}</div>
                    <div class="abc__digit no-sales">${detail.group_no_sales}</div>
                    <div class="abc__digit average-check">${detail.group_average_check}</div>        
                        `);
                    }
                    groupSummary.appendChild(periodItem);
                });
            });
            groupSummary.insertAdjacentHTML('beforeend',
                `<div class="abc__params">
                    <div class="abc__digit sales-vat">${group.group_sales_with_vat}</div>
                    <div class="abc__digit sales">${group.group_sales_without_vat}</div>
                    <div class="abc__digit profit">${group.group_profit}</div>
                    <div class="abc__digit quantity">${group.group_quantity}</div>
                    <div class="abc__digit no-sales">${group.group_no_sales}</div>
                    <div class="abc__digit average-check">${group.group_average_check}</div>        
                  </div>`);
            body.appendChild(groupDetail);
            if (group.customers) {
                group.customers.forEach(customer => {
                    const customerRow = document.createElement('div');
                    customerRow.classList.add(gridClass, 'abc');
                    customerRow.insertAdjacentHTML('afterbegin',
                        `<div>${customer.group_code}</div>
                  <div class="abc__params">
                    <div class="sales-vat">продажи с НДС</div>
                    <div class="sales">продажи без НДС</div>
                    <div class="profit">прибыль</div>
                    <div class="quantity">кол-во единиц (тыс.)</div>
                    <div class="average-check">кол-во продаж</divclass>
                    <div>средний чек</div>        
                  </div>`);
                    periodData.forEach(per => {
                        const periodItem = document.createElement('div');
                        periodItem.classList.add('abc__params');
                        customer.details.forEach(detail => {
                            if (detail.period_code === per.name) {
                                periodItem.insertAdjacentHTML("beforeend",
                                    `
                    <div class="abc__digit sales-vat">${detail.sales_with_vat_s}</div>
                    <div class="abc__digit sales">${detail.sales_without_vat_s}</div>
                    <div class="abc__digit profit">${detail.profit_s}</div>
                    <div class="abc__digit quantity">${detail.quantity_s}</div>
                    <div class="abc__digit no-sales">${detail.no_sales_s}</div>
                    <div class="abc__digit average-check">${detail.average_check_s}</div>        
                        `);
                                // return;
                            }
                            customerRow.appendChild(periodItem);
                        });
                    });
                    customerRow.insertAdjacentHTML('beforeend',
                        `<div class="abc__params">
                    <div class="abc__digit sales-vat">${customer.total_sales_with_vat}</div>
                    <div class="abc__digit sales">${customer.total_sales_without_vat}</div>
                    <div class="abc__digit profit">${customer.total_profit}</div>
                    <div class="abc__digit quantity">${customer.total_quantity}</div>
                    <div class="abc__digit no-sales">${customer.total_no_sales}</div>
                    <div class="abc__digit average-check">${customer.average_check}</div>        
                  </div>`);
                    groupDetail.appendChild(customerRow);
                });
            }
        });
    });
    return body;
}

