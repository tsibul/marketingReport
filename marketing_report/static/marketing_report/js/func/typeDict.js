'use strict'

import {dictList} from "../const/dictList.js";

/**
 * Take model name from current row id
 * @param row — row witn id= 'dictionary name'-id
 * @returns {*} — modelName
 */
export  function typeDict(row) {
    return dictList[row.id.split('-')[0]];
}