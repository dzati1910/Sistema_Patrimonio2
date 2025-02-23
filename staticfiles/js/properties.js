$(document).ready(() => {
    // Load properties on page load
    fetchProperties();

    // Handle property form submission
    $('#propertyForm').on('submit', function(e) {
        e.preventDefault();
        const data = $(this).serializeObject();
        $.ajax({
            type: 'POST',
            url: '/api/properties/',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function() {
                $('#createPropertyModal').modal('hide');
                fetchProperties();
                displayMessage('Bem criado com sucesso!', 'success');
            },
            error: function() {
                displayMessage('Erro ao criar bem.', 'danger');
            }
        });
    });
});

// Fetch and display properties
function fetchProperties() {
    $.get('/api/properties/', function(data) {
        $('#properties-table').empty();
        data.forEach(property => {
            $('<tr>')
                .append('<td>' + property.name + '</td>')
                .append('<td>' + property.category.name + '</td>')
                .append('<td>' + property.department.name + '</td>')
                .append('<td>' + property.rfid_tag + '</td>')
                .appendTo('#properties-table');
        });
    });
}