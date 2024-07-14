$(document).ready(function () {
    $('body').on('click', '.favorite-link', function (e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var link = $(this);
        $.ajax({
            url: link.attr('href'),
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function (response) {
                if (response.action === 'liked') {
                    link.html('❤️');
                } else {
                    link.html('🤍');
                }
            }
        });
    });
});
$(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});