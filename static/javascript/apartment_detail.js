
document.addEventListener('DOMContentLoaded', function () {

    (function () {
        const slider = document.querySelector('.apartment-slider');
        if (!slider) return;
        const slides = slider.querySelectorAll('.slide');
        const thumbs = slider.querySelectorAll('.thumb');
        const prevBtn = slider.querySelector('.prev');
        const nextBtn = slider.querySelector('.next');
        let current = 0;

        function showSlide(idx) {
            slides[current].classList.remove('active');
            thumbs[current].classList.remove('current');
            current = (idx + slides.length) % slides.length;
            slides[current].classList.add('active');
            thumbs[current].classList.add('current');
        }

        prevBtn.addEventListener('click', () => showSlide(current - 1));
        nextBtn.addEventListener('click', () => showSlide(current + 1));

        thumbs.forEach(thumb => {
            thumb.addEventListener('click', e => {
                showSlide(parseInt(e.currentTarget.dataset.index, 10));
            });
        });
    })();
});

