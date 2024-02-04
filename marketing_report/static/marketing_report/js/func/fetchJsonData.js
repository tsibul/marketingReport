'use strict'

/**
 * fetch data from json
 */
export function fetchJsonData(jsonUrl) {
    return fetch(jsonUrl)
        .then(response => response.json());
}