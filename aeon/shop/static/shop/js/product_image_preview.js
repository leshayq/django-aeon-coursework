document.addEventListener('DOMContentLoaded', function () {
    function showPreview(input) {
        const file = input.files[0];
        const parent = input.closest('.inline-related'); 

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const image = new Image();
                image.src = e.target.result;
                image.width = 100;  
                image.height = 100;

                let previewContainer = parent.querySelector('.image-preview-container');
                if (!previewContainer) {
                    previewContainer = document.createElement('div');
                    previewContainer.classList.add('image-preview-container');
                    input.parentNode.appendChild(previewContainer);  
                }

                previewContainer.innerHTML = '';
                previewContainer.appendChild(image); 
            };
            reader.readAsDataURL(file);  
        }
    }

    function addFileInputListeners() {
        const fileInputs = document.querySelectorAll('.inline-related input[type="file"]');
        fileInputs.forEach(function(input) {
            input.removeEventListener('change', handleFileChange); 
            input.addEventListener('change', handleFileChange); 
        });
    }

    function handleFileChange(event) {
        const input = event.target;
        showPreview(input); 
    }

    const observer = new MutationObserver(function(mutations) {
        addFileInputListeners();  
        checkImageCount();
    });

    const adminContent = document.querySelector('body');
    observer.observe(adminContent, { childList: true, subtree: true });

    addFileInputListeners();
    checkImageCount();

    function checkImageCount() {
        const imageCount = document.querySelectorAll('.inline-related input[type="file"]').length;
        const addButton = document.querySelector('.add-row');

        if (addButton) {
            if (imageCount >= 6) {
                addButton.style.display = 'none';  
            } else {
                addButton.style.display = '';  
            }
        }
    }
});
