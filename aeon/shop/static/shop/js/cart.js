$(document).on('click', '#add-button', function(e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: addToCartUrl,
        data: {
            product_id: $(this).val(),
            product_qty: 1,
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
        },
        success: function(response) {
            console.log('Product added:', response);
            window.location.href = "/cart/";
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
});

$(document).on('click', '#cart-delete-button', function(e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: deleteFromCartUrl,  
        data: {
            product_id: $(this).data('index'),
            csrfmiddlewaretoken: csrfToken, 
            action: 'post',
        },
        success: function(response) {
            document.getElementById('total').innerHTML = '<h1>Загальна сума: ' + response.total + '₴</h1>';
            location.reload();
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
});

function formatNumberWithCommas(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function changeQuantity(amount, productId) {
    const input = document.getElementById(`qtyInput${productId}`);
    let currentQty = parseInt(input.value);

    if (!isNaN(currentQty)) {
        const newQty = currentQty + amount;
        if (newQty >= input.min && newQty <= input.max) {
            input.value = newQty;
            updateCart(productId);
        }
    }
}

function updateCart(productId) {
    const input = document.getElementById(`qtyInput${productId}`);
    const productQty = parseInt(input.value);

    if (!isNaN(productQty)) {
        $.ajax({
            type: 'POST',
            url: updateCartUrl,
            data: {
                product_id: productId,
                product_qty: productQty,
                csrfmiddlewaretoken: csrfToken,
                action: 'post',
            },
            success: function(response) {
                // Обновляем общую сумму
                const totalPriceElement = document.getElementById('total');
                const formattedTotal = formatNumberWithCommas(response.total);
                totalPriceElement.innerHTML = '<h1>Загальна сума: ' + formattedTotal + '₴</h1>';

                // Обновляем цену конкретного товара в блоке "price"
                const priceElement = document.getElementById(`price-${productId}`);
                const formattedPrice = formatNumberWithCommas(response.item_total);
                priceElement.textContent = `₴${formattedPrice}`;

                // Обновляем количество и базовую цену в блоке "item-total"
                const itemTotalElement = document.getElementById(`item-total-${productId}`);
                itemTotalElement.textContent = `${response.item_qty} x ₴${formatNumberWithCommas(response.item_price)}`;
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    }
}