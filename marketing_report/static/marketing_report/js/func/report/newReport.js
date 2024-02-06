'use strict'

// add report block
import {temporaryNode} from "./temporaryNode.js";
import {changeReportBlockId} from "./changeReportBlockId.js";
import {addReportBlock} from "./addReportBlock.js";
import {addPeriodList} from "./addPeriodList.js";
import {addReportList} from "./addReportList.js";
import {buildReport} from "./buildReport.js";
import {reportRemove} from "./reportRemove.js";
import {selectFromList} from "../dropdown/selectFromList.js";
import {dropDownListenerVisible} from "../dropdown/dropDownListenerVisible.js";


/**
 *
 * @param thisObj
 * @param reportType
 */
export function newReport(thisObj, reportType) {
    let oldId = changeReportBlockId(thisObj);
    const tempNode = temporaryNode();
    thisObj.closest('.report-content').insertBefore(tempNode, thisObj.closest('.report-block'));
    setTimeout(function () {
        tempNode.style.width = '360px';
    }, 0);
    setTimeout(function () {
        tempNode.remove();
        const newNode = addReportBlock(reportType, oldId);
        newNode.classList.add('temp-width');
        newNode.querySelector('.btn-save').addEventListener('click', e => buildReport(e.target));
        newNode.querySelector('.btn-close').addEventListener('click', e => reportRemove(e.target));
        thisObj.closest('.report-content').insertBefore(newNode, thisObj.closest('.report-block'));
        addPeriodList(newNode);
        addReportList(newNode, reportType);
        const dropDownContentList = newNode.querySelectorAll('.dropdown__content');
        dropDownContentList.forEach(ul => {
            ul.previousElementSibling.querySelector('.dropdown__input')
                .addEventListener('click', e =>
                    dropDownListenerVisible(ul.closest('.dropdown'), e));
        });
        dropDownContentList[dropDownContentList.length - 1].querySelectorAll('li')
            .forEach(li =>
                li.addEventListener('click', e => selectFromList(e.target)));
    }, 300);
}
