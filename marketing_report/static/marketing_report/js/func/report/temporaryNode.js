'use strict'

export function temporaryNode() {
    const tempNode = document.createElement('div')
    tempNode.id = 'temp-node';
    tempNode.className = 'temp-block';
    return tempNode;
}
