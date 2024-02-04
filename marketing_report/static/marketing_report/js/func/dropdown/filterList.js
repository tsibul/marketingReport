'use strict'

/**
 *
 * @param input
 */
export function filterList(input) {
    let filter, ul, li, a, i;
    filter = input.value.toUpperCase();
    const div = input.closest('.dropdown');
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
