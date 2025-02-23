// Fetch CSRF token from cookie
function getCookie(name) {
    return decodeURIComponent(document.cookie.replace(new RegExp('(?:(?:^|.*;)\\s*' + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + '\\s*\\=\\s*([^;]*).*$)|^.*$'), '$1')) || '';
}

// Add CSRF header to all POST/PATCH/DELETE requests
$.ajaxSetup({
    headers: {
        'X-CSRFToken': getCookie('csrftoken')
    }
});

// Global message display
function displayMessage(message, type) {
    const alert = `<div class="alert alert-${type} alert-dismissible fade show">
        ${message} <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>`;
    $('#messages').append(alert);
}