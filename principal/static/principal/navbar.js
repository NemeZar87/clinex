document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggleButton');
    const links = document.querySelector('.nav-links');

    toggleButton.addEventListener('click', () => {
        links.classList.toggle('active');
    });
});
