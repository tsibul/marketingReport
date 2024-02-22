import {closeModal} from "./func/closeModal.js";
import {openModal} from "./func/openModal.js";

const authModal = document.getElementById('authModal');
const closeButtons = document.querySelectorAll('.login__close');
const loginForm = document.getElementById('login-form');
const logoutForm = document.getElementById('logout-form');
// const badges = document.querySelectorAll('.menu__item_badge');

// fillBadges(badges);

closeButtons.forEach(row => {
    row.addEventListener("click", (e) => {
        closeModal(e.target);
    });
});

// При клике на кнопку "вход" отображаем форму входа и скрываем форму выхода
document.getElementById('login-button').addEventListener('click', function () {
    loginForm.style.display = 'block';
    logoutForm.style.display = 'none';
    openModal(authModal);
});

// При клике на кнопку "выход" отображаем форму выхода и скрываем форму входа
document.getElementById('logout-button').addEventListener('click', function () {
    logoutForm.style.display = 'block';
    loginForm.style.display = 'none';
    openModal(authModal);
});

// function fillBadges(badges) {
//     const badgeImport = document.querySelector('.badges').value;
//     if(badgeImport) {
//         const badgeData = JSON.parse(badgeImport);
//         let i = 0;
//         badges.forEach(badge => {
//             if (badgeData[i]) {
//                 badge.setAttribute('data-badge', badgeData[i]);
//             }
//             i++;
//         });
//     }
// }