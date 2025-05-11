document.addEventListener('DOMContentLoaded', function() {
    const deliveryTypeSelect = document.getElementById('delivery_type');
    const fields = {
        email: document.getElementById('field_email'),
        full_name: document.getElementById('field_full_name'),
        number: document.getElementById('field_number'),
        address: document.getElementById('field_address'),
        city: document.getElementById('field_city'),
        department: document.getElementById('field_department')
    };

    function hideAllFields() {
        Object.values(fields).forEach(field => field.style.display = 'none');
    }

    function showFieldsForDeliveryType(type) {
        hideAllFields();
        fields.email.style.display = 'block';
        fields.full_name.style.display = 'block';
        fields.number.style.display = 'block';

        if (type === "Кур'єр по місту") {
            fields.address.style.display = 'block';
            fields.city.style.display = 'block';
        } else if (type === 'Доставка у відділення') {
            fields.city.style.display = 'block';
            fields.department.style.display = 'block';
        }
    }

    deliveryTypeSelect.addEventListener('change', function() {
        showFieldsForDeliveryType(this.value);
    });

    hideAllFields();
});