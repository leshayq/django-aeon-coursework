$(document).ready(function() {
    const activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        loadTabContent($(`.menu-item[data-tag="${activeTab}"]`).attr('href'));
    }

    $('.menu-item').on('click', function(event) {
        if ($(this).data('no-ajax')) {
            return;
        }

        event.preventDefault();
        const url = $(this).attr('href');
        const tab = $(this).data('tag');
        localStorage.setItem('activeTab', tab);

        loadTabContent(url);
    });

    function loadTabContent(url) {
        $.ajax({
            url: url,
            method: 'GET',
            success: function(data) {
                $('.profile-content').html(data);
            },
            error: function(xhr, status, error) {
                console.error('Помилка завантаження: ' + error);
            }
        });
    }
});