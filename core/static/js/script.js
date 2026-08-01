document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (!navToggle || !navLinks) {
        return;
    }

    const closeMenu = () => {
        navLinks.classList.remove('open');
        navToggle.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Abrir menu');
    };

    navToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('open');
        navToggle.classList.toggle('open', isOpen);
        navToggle.setAttribute('aria-expanded', String(isOpen));
        navToggle.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');
    });

    navLinks.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', closeMenu);
    });

    document.addEventListener('click', (event) => {
        const clickedInsideNav = navToggle.contains(event.target) || navLinks.contains(event.target);

        if (!clickedInsideNav && navLinks.classList.contains('open')) {
            closeMenu();
        }
    });
});
