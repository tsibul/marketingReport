'use strict'

import {createEditForm} from "./func/createEditForm.js";
import {cancelEditRecord} from "./func/cancelEditRecord.js";
import {normalizeSearchString} from "./func/normalizeSearchString.js";
import {appendNewRows} from "./func/appendNewRows.js";
import {copyRowFromHidden} from "./func/copyRowFromHidden.js";
import {deleteRecord} from "./func/deleteRecord.js";
import {userRights} from "./func/userRights.js";
import {normalizeSearchStringValue} from "./func/normalizeSearchStringValue.js";
import {clearSearch} from "./func/clearSearch.js";
import {handleDragEnter, handleDragLeave, handleDragOver} from "./func/dictionary/handlersDnD.js";
import {hideDict} from "./func/dictionary/hideDict.js";
import {showDict} from "./func/dictionary/showDict.js";
import {initDictionary} from "./func/dictionary/initDictionary.js";


const addButtons = document.querySelectorAll('.btn_add');
const searchButtons = document.querySelectorAll('.search_submit');
const searchClearButtons = document.querySelectorAll('.search_clear')
const showDeleted = document.getElementById('showDeleted') ? 1 : 0;
const dictBlockContent = document.querySelectorAll('.dict-block__content');
const dictBlockList = document.querySelectorAll('.dict-block');
const dictStartChecks = document.querySelectorAll('.checkbox-out');
const rightField = document.querySelector('.dict-right');
const hiddenBlock = document.querySelector('.dict');
let dragSrcEl = null;

dictStartChecks.forEach(chck => {
    chck.addEventListener('change', e => {
        const dictToFind = e.target.id + '-0';
        const dictToCopy = document.getElementById(dictToFind).closest('.dict-block');
        const dictDetails = e.target.closest('.dict-menu__details');
        const dictHeader = dictDetails.querySelector('.dict-menu__header');
        if (chck.checked) {
            showDict(rightField, dictToCopy, dictHeader, e.target);
        } else {
            hideDict(hiddenBlock, dictToCopy, dictHeader, dictDetails, e.target);
        }
    });
    chck.addEventListener('click', async e => {
        await initDictionary(e.target, showDeleted);
    }, {once: true});

});

/**
 * prevent open close details on 'space'
 */
window.onload = function () {
    const summary = document.querySelectorAll('.dict-block__header_block-space');
    const fn = function (e) {
        if (e.keyCode === 32) {
            e.preventDefault();
        }
    };
    summary.forEach(el => {
        el.onkeyup = fn;
    });
};

userRights();

/**
 * listener for DnD
 */
dictBlockList.forEach(block => {
    block.addEventListener('dragstart', handleDragStart, false);
    block.addEventListener('dragover', handleDragOver, false);
    block.addEventListener('dragenter', handleDragEnter);
    block.addEventListener('dragleave', handleDragLeave);
    block.addEventListener('drop', handleDrop, false);
    block.addEventListener('dragend', handleDragEnd);
});

/**
 * listener if your click outside the form — close form
 */
addEventListener('mousedown', function (element) {
    try {
        const parentRow = document.querySelector('form').closest('.dict-block__row')
        if (element.target !== parentRow && !parentRow.contains(element.target)) {
            const buttonClose = document.querySelector('form').querySelector('.btn-close');
            cancelEditRecord(buttonClose);
        }
    } catch (exception) {
    }
});

/**
 * listener to append new records to dictionary when you over the last showed
 */
dictBlockContent.forEach(block => {
    block.addEventListener('mouseover', async e => {
        const lastRecord = block.querySelector('div[data-last]:not([data-last = ""])')
        if (e.target === lastRecord) {
            let searchString = normalizeSearchString(lastRecord);
            if (!searchString) {
                searchString = '';
            }
            await appendNewRows(lastRecord, block, searchString, 0, 0);
        }
    });
});


/**
 * Listener for new record in dictionary
 * Catch click on addButtons
 * add new row then edit
 */
addButtons.forEach(btn => {
    btn.addEventListener('click', async event => {
        event.preventDefault();
        await addButtonEvent(event, btn);
    });
});

/**
 * Listener for '.dict-block__row'
 * edit for click on all element
 * delete element for click on button '.btn-delete'
 */
dictBlockContent.forEach(block => {
    block.addEventListener('click', async e => {
        const dictBlockRow = block.querySelectorAll('.dict-block__row');
        for (const row of dictBlockRow) {
            await editDeleteRow(e, row);
        }
    });
});


// Search
/**
 * renew dict records according to search conditions
 */
searchButtons.forEach((btn) => {
    btn.addEventListener('mousedown', async (search) => {
        const btnEvent = searchButtonEvent(btn, search);
        await appendNewRows(btnEvent[0], btnEvent[2], btnEvent[1], showDeleted, 0);
        btnEvent[0].remove();
    });
});

/**
 * listener for clear search input
 */
searchClearButtons.forEach(btn => {
    btn.addEventListener('click', e => {
        clearSearch(btn);
    });
});

/**
 *
 * @param e
 * @param row
 */
async function editDeleteRow(e, row) {
    if (row === e.target.closest('.dict-block__row')) {
        if (e.target.classList.contains('btn_delete')) {
            await deleteRecord(row, showDeleted);
        } else {
            await createEditForm(e.target.closest('.dict-block__row'));
        }
    }
}

/**
 *
 * @param btn
 * @param search
 * @returns {Promise<void>}
 */
function searchButtonEvent(btn, search) {
    const dictBlock = search.target.closest('.dict-block');
    const searchValue = normalizeSearchStringValue(dictBlock);
    const dictBlockContent = dictBlock.querySelector('.dict-block__content');
    const hiddenRow = dictBlockContent.querySelector('.dict-block__row_hidden');
    const temporaryRow = hiddenRow.cloneNode(true)
    temporaryRow.setAttribute('data-last', '0');
    dictBlockContent.appendChild(temporaryRow);
    dictBlockContent.innerHTML = '';
    dictBlockContent.appendChild(hiddenRow);
    return [temporaryRow, searchValue, dictBlockContent];
}

/**
 *
 * @param event
 * @param btn
 */
async function addButtonEvent(event, btn) {
    if (event.target === btn) {
        const dictBlock = btn.closest('.dict-block');
        const copyRow = dictBlock.querySelector('.dict-block__row_hidden');
        const newRow = copyRowFromHidden(copyRow);
        await createEditForm(newRow);
    }
}

/**
 * DnD handler functions
 */

/**
 * handle drag start function
 * obtain data from dragged element
 * @param event
 */
function handleDragStart(event) {
    dragSrcEl = this;
    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.setData('text/html', this.innerHTML);
}


/**
 * handle drag drop functions
 * exchange inner HTML's between blocks
 * then return event listeners to elements
 * @param event
 * @returns {boolean}
 */
function handleDrop(event) {
    if (dragSrcEl !== this) {
        const sourceClasses = dragSrcEl.className;
        dragSrcEl.className = this.className;
        this.className = sourceClasses;

        dragSrcEl.innerHTML = this.innerHTML;
        this.innerHTML = event.dataTransfer.getData('text/html');

        /**
         * return listeners for target block
         */
        const thisSearchSubmit = this.querySelector('.search_submit');
        const thisBlock = this.querySelector('.dict-block__content');
        thisBlock.querySelectorAll('div').forEach(row => {
            row.addEventListener('click', async e => {
                await editDeleteRow(e, row);
            });
        });
        this.querySelector('.btn_add').addEventListener('click', async e => {
            await addButtonEvent(e, this.querySelector('.btn_add'));
        });
        if (thisSearchSubmit) {
            thisSearchSubmit.addEventListener('click', async e => {
                const btnEvent = searchButtonEvent(thisSearchSubmit, e);
                await appendNewRows(btnEvent[0], btnEvent[2], btnEvent[1], showDeleted, 0);
                btnEvent[0].remove();
            });
            thisSearchSubmit.nextElementSibling.addEventListener('click', e => {
                clearSearch(e.target);
            });
        }
        thisBlock.addEventListener('mouseover', async e => {
            const lastRecord = thisBlock.querySelector('div[data-last]:not([data-last = ""])')
            if (e.target === lastRecord) {
                let searchString = normalizeSearchString(lastRecord);
                if (!searchString) {
                    searchString = '';
                }
                const nextRecords = await appendNewRows(lastRecord, thisBlock, searchString, 0, 0);
                for (let i = 0; i < nextRecords.length; i++) {
                    nextRecords[i].addEventListener('click', e => {
                        editDeleteRow(e, nextRecords[i]);
                    });
                }
            }
        });
        /**
         * return listeners for source block
         */
        const srcSearchSubmit = dragSrcEl.querySelector('.search_submit');
        const dragBlock = dragSrcEl.querySelector('.dict-block__content');
        dragBlock.querySelectorAll('div').forEach(row => {
            row.addEventListener('click', async e => {
                await editDeleteRow(e, row);
            });
        });
        dragSrcEl.querySelector('.btn_add').addEventListener('click', async e => {
            await addButtonEvent(e, dragSrcEl.querySelector('.btn_add'));
        });
        if (srcSearchSubmit) {
            srcSearchSubmit.addEventListener('click', async e => {
                const btnEvent = searchButtonEvent(srcSearchSubmit, e);
                await appendNewRows(btnEvent[0], btnEvent[2], btnEvent[1], showDeleted, 0);
                btnEvent[0].remove();
            });
            srcSearchSubmit.nextElementSibling.addEventListener('click', e => {
                clearSearch(e.target);
            });
        }
        dragBlock.addEventListener('mouseover', async e => {
            const lastRecord = dragBlock.querySelector('div[data-last]:not([data-last = ""])')
            if (e.target === lastRecord) {
                e.preventDefault();
                let searchString = normalizeSearchString(lastRecord);
                if (!searchString) {
                    searchString = '';
                }
                const nextRecords = await appendNewRows(lastRecord, dragBlock, searchString, 0, 0);
                for (let i = 0; i < nextRecords.length; i++) {
                    nextRecords[i].addEventListener('click', e => {
                        editDeleteRow(e, nextRecords[i]);
                    });
                }
            }
        });
    }
    return false;
}

/**
 * handle drag function
 * remove class 'over' from draggable elements
 * when dropped
 * @param event
 */
function handleDragEnd(event) {
    dictBlockList.forEach(block => {
        block.querySelector('.dict-block__header').classList.remove('over')
    });
}
