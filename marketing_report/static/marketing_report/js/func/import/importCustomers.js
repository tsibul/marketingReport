'use strict'

import {fetchJsonData} from "../fetchJsonData.js";

export async function importCustomers(url) {
    const counts = await fetchJsonData('/marketing/' + url);
    const newCustomers = document.getElementById(url);
    newCustomers.textContent = `импортировано ${counts.result}`;
}
