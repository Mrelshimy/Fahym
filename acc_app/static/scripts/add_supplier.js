$(document).ready(function () {
  $('.add-item-form').on('submit', function (event) {
    // Prevent the default form submission
    event.preventDefault();

    const formData = {
      code: $('#code').val(),
      name: $('#name').val(),
      email: $('#email').val(),
      address: $('#address').val(),
      phone: $('#phone').val(),
      user_id: userId
    };

    $.ajax({
      method: 'POST',
      url: `http://localhost:5001/acc_app/api/v1/users/${formData.user_id}/suppliers`,
      contentType: 'application/json',
      data: JSON.stringify(formData),
      success: function (response) {
        console.log('Supplier added successfully:', response);
        // Reset Form
        $('.add-item-form')[0].reset();
        alert('Supplier added successfully');
      },
      error: function (xhr, status, error) {
        // Display Error Message
        console.error('Error adding supplier:', error);
      }
    });
  });
});
