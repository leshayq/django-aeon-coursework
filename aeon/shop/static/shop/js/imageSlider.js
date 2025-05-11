document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("slider");
    const images = document.querySelectorAll(".slider-image");
    const thumbnails = document.querySelectorAll(".thumbnail");
    let currentIndex = 0;

    const updateSlider = (index) => {
        slider.style.transform = `translateX(-${index * 100}%)`;
        thumbnails.forEach((thumb, i) => {
            thumb.classList.toggle("active", i === index);
        });
    };

    document.getElementById("prev-btn").addEventListener("click", () => {
        currentIndex = (currentIndex > 0) ? currentIndex - 1 : images.length - 1;
        updateSlider(currentIndex);
    });

    document.getElementById("next-btn").addEventListener("click", () => {
        currentIndex = (currentIndex < images.length - 1) ? currentIndex + 1 : 0;
        updateSlider(currentIndex);
    });

    thumbnails.forEach((thumb, index) => {
        thumb.addEventListener("click", () => {
            currentIndex = index;
            updateSlider(currentIndex);
        });
    });


    updateSlider(currentIndex);
});