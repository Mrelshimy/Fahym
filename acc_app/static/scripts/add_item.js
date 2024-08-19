$(document).ready(function () {
  $('.add-item-form').on('submit', function (event) {
    // Prevent the default form submission
    event.preventDefault();

    const formData = {
      code: $('#code').val(),
      name: $('#name').val(),
      unit: $('#unit').val(),
      description: $('#description').val(),
      purchase_price: $('#purchase-price').val(),
      sales_price: $('#sales-price').val(),
      stock: $('#stock').val(),
      user_id: userId
    };

    $.ajax({
      method: 'POST',
      url: `http://localhost:5001/acc_app/api/v1/users/${formData.user_id}/items`,
      contentType: 'application/json',
      data: JSON.stringify(formData),
      success: function (response) {
        console.log('Item added successfully:', response);
        // Reset Form
        $('.add-item-form')[0].reset();
        alert('Item added successfully');
      },
      error: function (xhr, status, error) {
        // Display Error Message
        console.error('Error adding item:', error);
      }
    });
  });
});
