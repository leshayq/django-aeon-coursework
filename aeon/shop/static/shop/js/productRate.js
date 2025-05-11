const rate = (rating, product_id) => {
    fetch(`/rate/${product_id}/${rating}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            
            window.location.href = data.redirect_url;
        } else {
            
            window.location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}