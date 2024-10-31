document.querySelector('.searchbar input[type="text"]').addEventListener('input', function () {
    const searchResults = document.getElementById('search-results');
    if (this.value) {
        searchResults.classList.add('show');
    } else {
        searchResults.classList.remove('show');
    }
    });