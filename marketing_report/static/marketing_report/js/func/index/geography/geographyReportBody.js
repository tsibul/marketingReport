'use strict'

import {createPeriodRow} from "../createPeriodRow.js";
import {createParameterRow} from "../abc/abcReportBody.js";

export function geographyReportBody(report) {
    const body = document.createElement('div');
    body.appendChild(createParameterRow());
    const perData = createPeriodRow(report);

    const periodData = perData[0];
    const gridClass = perData[1];
    const periodRow = perData[2];
    body.appendChild(periodRow)

    report.report.report_data.forEach(region => {
        let regionDetail = document.createElement('details');
        let regionSummary = document.createElement('summary');
        regionSummary.classList.add('abc', gridClass, 'abc__summary', 'unit-title');
        regionDetail.appendChild(regionSummary);
        const unitTitle = 'Регион ' + Object.keys(region)[0];
        regionSummary.insertAdjacentHTML('afterbegin',
            `<div>${unitTitle}</div>
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
            let regionSales;
            Object.values(region)[0].forEach(dict => {
                if (Object.keys(dict).includes('region_sales')) {
                    regionSales = dict['region_sales'];
                }
            });
            regionSales.forEach(detail => {
                if (detail.period__name === per.name) {
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
                regionSummary.appendChild(periodItem);
            });
        });
        let regionTotalSales;
        Object.values(region)[0].forEach(dict => {
            if (Object.keys(dict).includes('total_sales')) {
                regionTotalSales = dict['total_sales'][0];
            }
        });
        regionSummary.insertAdjacentHTML('beforeend',
            `<div class="abc__params">
                    <div class="abc__digit sales-vat">${regionTotalSales.sales_with_vat_s}</div>
                    <div class="abc__digit sales">${regionTotalSales.sales_without_vat_s}</div>
                    <div class="abc__digit profit">${regionTotalSales.profit_s}</div>
                    <div class="abc__digit quantity">${regionTotalSales.quantity_s}</div>
                    <div class="abc__digit no-sales">${regionTotalSales.no_sales_s}</div>
                    <div class="abc__digit average-check">${regionTotalSales.average_check_s}</div>        
                  </div>`);
        body.appendChild(regionDetail);
        Object.values(region)[0].forEach(dict => {
            if (Object.keys(dict).length !== 1) {
                let unitDetails = document.createElement('details');
                let unitSummary = document.createElement('summary');
                unitSummary.classList.add('abc', gridClass, 'abc__summary');
                unitSummary.insertAdjacentHTML('afterbegin',
                    `<div>${Object.keys(dict)[0]}</div>
                        <div class="abc__params">
                        <div class="sales-vat">продажи с НДС</div>
                        <div class="sales">продажи без НДС</div>
                        <div class="profit">прибыль</div>
                        <div class="quantity">кол-во единиц (тыс.)</div>
                        <div class="no-sales">кол-во продаж</div>
                        <div class="average-check">средний чек</div>        
                      </div>`);
                unitDetails.appendChild(unitSummary);
                regionDetail.appendChild(unitDetails);
                periodData.forEach(per => {
                    const periodItem = document.createElement('div');
                    periodItem.classList.add('abc__params');
                    let unitSales = dict['unit_sales'];
                    unitSales.forEach(detail => {
                        if (detail.period__name === per.name) {
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
                        unitSummary.appendChild(periodItem);
                    });
                });
                unitSummary.insertAdjacentHTML('beforeend',
                    `
                    <div class="abc__digit sales-vat">${dict['total_sales'][0].sales_with_vat_s}</div>
                        <div class="abc__digit sales">${dict['total_sales'][0].sales_without_vat_s}</div>
                        <div class="abc__digit profit">${dict['total_sales'][0].profit_s}</div>
                        <div class="abc__digit quantity">${dict['total_sales'][0].quantity_s}</div>
                        <div class="abc__digit no-sales">${dict['total_sales'][0].no_sales_s}</div>
                        <div class="abc__digit average-check">${dict['total_sales'][0].average_check_s}
                    </div>`
                );

                Object.values(dict)[0].forEach(item => {
                    let customerRow = document.createElement('div');
                    customerRow.classList.add('abc', gridClass);
                    unitDetails.appendChild(customerRow);
                    customerRow.insertAdjacentHTML('afterbegin',
                        `<div>${Object.keys(item)[0]}</div>
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
                        Object.values(item)[0].forEach(detail => {
                            if (detail.period__name === per.name) {
                                periodItem.insertAdjacentHTML("beforeend",
                                    `
                                        <div class="abc__digit sales-vat">${detail.sales_with_vat_s}</div>
                                        <div class="abc__digit sales">${detail.sales_without_vat_s}</div>
                                        <div class="abc__digit profit">${detail.profit_s}</div>
                                        <div class="abc__digit quantity">${detail.quantity_s}</div>
                                        <div class="abc__digit no-sales">${detail.no_sales_s}</div>
                                        <div class="abc__digit average-check">${detail.average_check_s}</div>        
                                    `);
                            }
                            customerRow.appendChild(periodItem);
                        });
                    });
                });
            }
        });


    });


    return body;

}