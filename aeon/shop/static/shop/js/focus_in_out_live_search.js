const searchInput = document.querySelector('.searchbar input[type="text"]');
const searchResults = document.getElementById('search-results');

searchInput.addEventListener('focus', () => {
    if (searchInput.value.trim() !== '') {
        searchResults.classList.add('show');
    }
});

searchInput.addEventListener('focusout', (event) => {
    setTimeout(() => {
        if (!searchResults.contains(document.activeElement)) {
            searchResults.classList.remove('show');
        }
    }, 150);
});

searchInput.addEventListener('input', () => {
    if (searchInput.value.trim() === '') {
        searchResults.classList.remove('show');
    }
});
