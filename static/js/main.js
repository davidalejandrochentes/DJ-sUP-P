window.sr = ScrollReveal();

sr.reveal('.animacion', {
    duration: 2900,
    origin: 'top',
    distance: '-20px',
});

sr.reveal('.animacion-derecha', {
    duration: 2900,
    origin: 'right',
    distance: '-50px',
});

sr.reveal('.animacion-izquierda', {
    duration: 2900,
    origin: 'left',
    distance: '-50px',
});

sr.reveal('.animacion-arriba', {
    duration: 2900,
    origin: 'top',
    distance: '-50px',
});

sr.reveal('.animacion-bajo', {
    duration: 2900,
    origin: 'top',
    distance: '50px',
});

sr.reveal('.modal', { reset: false }, { afterReveal: null });