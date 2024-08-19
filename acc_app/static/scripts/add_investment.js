$(document).ready(function () {
  $('.add-item-form').on('submit', function (event) {
    // Prevent the default form submission
    event.preventDefault();

    const formData = {
      name: $('#name').val(),
      date: $('#date').val(),
      remarks: $('#remarks').val(),
      amount: $('#amount').val(),
      user_id: userId
    };

    $.ajax({
      method: 'POST',
      url: `http://localhost:5001/acc_app/api/v1/users/${formData.user_id}/investments`,
      contentType: 'application/json',
      data: JSON.stringify(formData),
      success: function (response) {
        console.log('Investment added successfully:', response);
        // Reset Form
        $('.add-item-form')[0].reset();
        alert('Investment added successfully');
      },
      error: function (xhr, status, error) {
        // Display Error Message
        console.error('Error adding investment:', error);
      }
    });
  });
});
