function fetchJsonData(jsonUrl) {
    return fetch(jsonUrl)
        .then(response => response.json());
}
