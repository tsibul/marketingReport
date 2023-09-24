document.addEventListener('click', element => {
    const dropdown = document.querySelectorAll('.dropdown');
    let obj;
    dropdown.forEach(element => {
        if (element.querySelector('ul').classList.contains('visible')) {
            obj = element;
        }
    });
    if (obj != null && !obj.contains(element.target)) {
        obj.querySelector('ul').classList.remove('visible');
        obj.querySelector('.dropdown__input').value = obj.querySelector('.dropdown__input').dataset.value;
    }
});

document.addEventListener('click', element => {
    const dropdown = document.querySelectorAll('.dropdown');
    dropdown.forEach(dropChild => {
        if (dropChild.contains(element.target)) {
            dropChild.querySelector('ul').classList.add('visible');
        }
    });
});


function fetchJsonData(jsonUrl) {
    return fetch(jsonUrl)
        .then(response => response.json());
}

function filterList(input) {
    let filter, ul, li, a, i;
    filter = input.value.toUpperCase();
    const div = input.parentElement.parentElement;
    a = div.getElementsByTagName("li");
    for (i = 0; i < a.length; i++) {
        let txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

function selectFromList(obj) {
    obj.parentElement.parentElement.querySelector('.dropdown__input').value = obj.textContent;
    obj.parentElement.parentElement.querySelector('.dropdown__input').dataset.value = obj.textContent;
    obj.parentElement.parentElement.querySelector('.dropdown__hidden').value = obj.dataset.value;
    obj.parentElement.classList.remove('visible');
}
