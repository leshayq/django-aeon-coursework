document.addEventListener('DOMContentLoaded', function () {
    const imageField = document.querySelector('input[type="file"][name$="image"]');
    if (imageField) {
        const previewContainer = document.createElement('div');
        previewContainer.classList.add('image-preview-container');
        imageField.parentNode.appendChild(previewContainer);

        imageField.addEventListener('change', function () {
            const file = imageField.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewContainer.innerHTML = `<img src="${e.target.result}" width="200" style="margin-top: 10px;" />`;
                };
                reader.readAsDataURL(file);
            } else {
                previewContainer.innerHTML = '';
            }
        });
    }
});
