document.addEventListener('DOMContentLoaded', function () {
  // Run this code only after the whole page has loaded

  (function () {
    // Find the main slider container
    const slider = document.querySelector('.apartment-slider');
    if (!slider) return; // Stop if no slider found on the page

    // Get all the slides and thumbnails inside the slider
    const slides = slider.querySelectorAll('.slide');
    const thumbs = slider.querySelectorAll('.thumb');

    // Get the buttons to go previous and next
    const prevBtn = slider.querySelector('.prev');
    const nextBtn = slider.querySelector('.next');

    let current = 0; // Track the current slide index

    // Function to show a slide by index
    function showSlide(idx) {
      // Remove active styles from current slide and thumb
      slides[current].classList.remove('active');
      thumbs[current].classList.remove('current');

      // Calculate new index, looping around if needed
      current = (idx + slides.length) % slides.length;

      // Add active styles to new slide and thumb
      slides[current].classList.add('active');
      thumbs[current].classList.add('current');
    }

    // When prev button clicked, show previous slide
    prevBtn.addEventListener('click', () => showSlide(current - 1));

    // When next button clicked, show next slide
    nextBtn.addEventListener('click', () => showSlide(current + 1));

    // When a thumbnail is clicked, show that slide
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', e => {
        // Use data-index attribute to know which slide to show
        showSlide(parseInt(e.currentTarget.dataset.index, 10));
      });
    });
  })();
});
