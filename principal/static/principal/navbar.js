// document.addEventListener('DOMContentLoaded', () => {
//     const toggleButton = document.getElementById('toggleButton');
//     const links = document.querySelector('.nav-links');

//     toggleButton.addEventListener('click', () => {
//         links.classList.toggle('active');
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    // Hamburguesa principal
    const toggleButton = document.getElementById('toggleButton');
    const links = document.getElementById('navBarLinks');

    toggleButton.addEventListener('click', (e) => {
        e.stopPropagation(); // <-- Evita que el click llegue al document
        links.classList.toggle('active');
    });

    // Menú extra
    const menu2Button = document.getElementById('toggleMenu2');
    const menu2 = document.getElementById('menu2');

    menu2Button.addEventListener('click', (e) => {
        e.stopPropagation(); // <-- Evita que el click llegue al document
        menu2.classList.toggle('activo');
    });

    // Cerrar al tocar fuera
    document.addEventListener('click', function(e) {
        if (!links.contains(e.target)) {
            links.classList.remove('active');
        }
        if (!menu2.contains(e.target)) {
            menu2.classList.remove('activo');
        }
    });
});
