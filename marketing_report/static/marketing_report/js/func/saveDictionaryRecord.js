'use strict'

import {saveEditForm} from "./saveEditForm.js";
import {dictList} from "../const/dictList.js";

/**
 *
 * @param obj
 */
export function saveDictionaryRecord(obj) {
    event.preventDefault();
    const updateForm = obj.closest('.form-row');
    const dictionaryType = updateForm.parentElement.id.split('-')[0];
    const fetchPath = '/marketing/dict_update/' + dictList[dictionaryType];
    saveEditForm(updateForm, fetchPath)
}
