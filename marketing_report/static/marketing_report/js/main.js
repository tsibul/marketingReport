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