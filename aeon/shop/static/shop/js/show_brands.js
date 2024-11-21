$(document).on('click', '#show-more-brands', function() {
    showMoreBrands();
});

function showMoreBrands() {
    var moreBrands = document.getElementById("more-brands");
    var button = document.getElementById("show-more-brands");

    if (moreBrands.style.display === "none") {
        moreBrands.style.display = "block";
        button.style.display = 'none';
    }

}