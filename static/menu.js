// JavaScript para el menú desplegable
document.addEventListener('DOMContentLoaded', function () {
    var dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function (dropdown) {
        var trigger = dropdown.querySelector('.dropbtn');
        var content = dropdown.querySelector('.dropdown-content');

        trigger.addEventListener('click', function () {
            content.style.display = (content.style.display === 'block') ? 'none' : 'block';
        });
    });
});
