$(document).on('click', '.toggle-details', function() {
    const id = $(this).data('details-id');
    toggleDetails(id, this);
});

function toggleDetails(id, button) {
    const details = document.getElementById(id);
    const icon = button.querySelector('.icon');
    
    if (details.style.display === "none") {
        details.style.display = "block";
        icon.textContent = '×';
    } else {
        details.style.display = "none";
        icon.textContent = '+'; 
    }
}