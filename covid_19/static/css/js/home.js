document.addEventListener("DOMContentLoaded", function () {
  const sliderContainer = document.querySelector(".slider-container");
  const slides = document.querySelectorAll(".slide");

  let currentIndex = 0;
  let direction = 1; // 1 for forward, -1 for backward

  function nextSlide() {
    currentIndex += direction;

    if (currentIndex === slides.length) {
      // If reached the last photo, change direction to move backward
      currentIndex = slides.length - 2;
      direction = -1;
    } else if (currentIndex < 0) {
      // If reached the first photo, change direction to move forward
      currentIndex = 1;
      direction = 1;
    }

    updateSlider();
  }

  function updateSlider() {
    const translateValue = -currentIndex * 100 + "%";

    // Set transition duration only when changing slide
    sliderContainer.style.transition = "transform 1s ease-in-out";
    sliderContainer.style.transform = "translateX(" + translateValue + ")";
  }

  // Reset transition duration after the transition ends
  sliderContainer.addEventListener("transitionend", function () {
    sliderContainer.style.transition = "";
  });

  setInterval(nextSlide, 3000); // Change slide every 3 seconds (adjust as needed)
});
