'use strict'

/**
 * Reformat datetime received from html to format which recognize by DB
 * @param dateString datetime receive from html format dd.mm.YYYY HH:ii
 * @returns {string} datetime for db to recognize YYYY-MM-DDHH:ii
 */
export function stringToDateTime(dateString) {
    const parts = dateString.split(" ");
    const dateParts = parts[0].split(".");
    const time = parts[1];
    const year = '20' + dateParts[2]; // Преобразовать двузначный год в четырёхзначный
    const month = dateParts[1];
    const day = dateParts[0];
    return `${year}-${month}-${day}T${time}`;
}