'use strict'

import {fetchJsonData} from "../fetchJsonData.js";

export async function editTemporaryBase() {
    const counts = await fetchJsonData('/marketing/edit_temporary_base');
    const newCustomers = document.getElementById('new-customers');
    const updatedCustomers = document.getElementById('updated-customers');
    newCustomers.textContent = `новые ${counts.new_customers}`;
    updatedCustomers.textContent = `измененные ${counts.updated_customers}`;
}
