'use strict'

import {typeDict} from "./typeDict.js";

export async function deleteRecord(row, showDeleted) {
    const idNo = row.dataset.id;
    const dictType = typeDict(row);
    const url = `/production/dict_delete/${dictType}/${idNo}`;
    showDeleted ? row.querySelector(`[data-name = "deleted"]`).textContent = 'Да' : row.remove();
    await fetch(url);
}

