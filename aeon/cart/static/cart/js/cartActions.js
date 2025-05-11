document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.qty-btn').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('.qty-input');
            let value = parseInt(input.value);
            
            if (this.dataset.action === 'decrease') {
                if (value > 1) {
                    input.value = value - 1;
                }
            } else {
                input.value = value + 1;
            }
            
            this.closest('form').submit();
        });
    });
    
    document.querySelectorAll('.quantity-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const itemRow = this.closest('tr');
                    itemRow.querySelector('.item-total').textContent = data.item_price + ' грн.';
                    document.getElementById('cart-total').textContent = data.cart_price + ' грн.';
                }
            });
        });
    });
    
    document.querySelectorAll('.remove-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const itemRow = this.closest('tr');
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    itemRow.remove();
                    
                    document.getElementById('cart-total').textContent = data.cart_price + ' грн.';
                    
                    if (data.cart_total === 0) {
                        window.location.reload();
                    }
                }
            });
        });
    });
});