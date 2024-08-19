$(document).ready(() => {
  $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/customers`,
    contentType: 'application/json',
    success: function (response) {
      customers = response;
      if (customers.length === 0) { // Check for empty array
        console.log('No items found!');
        const emptyRow = `
            <tr>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
            </tr>`;
        $('.items-table tbody').append(emptyRow);
      } else {
        console.log('customers retrieved successfully:', response);
        response.forEach(customer => {
          const row = `
              <tr data-id="${customer.id}">
                  <td>${customer.name}</td>
                  <td>${customer.code}</td>
                  <td>${customer.email}</td>
                  <td>${customer.phone}</td>
                  <td><a href="#" class="delete-item">Delete</a></td>
              </tr>`;
          $('.items-table tbody').append(row);
        });
      }
    },
    error: function (xhr, status, error) {
      // Display Error Message
      console.error('Error getting customers:', error);
    }
  });

  $('.items-table tbody').on('click', '.delete-item', function (event) {
    event.preventDefault();
    if (confirm('Are you sure you want to delete this customer?')) {
      const row = $(this).closest('tr');
      const custId = row.data('id'); // Get the item ID from the data attribute
      console.log('Deleting customer ID:', custId);

      $.ajax({
        method: 'DELETE',
        url: `http://localhost:5001/acc_app/api/v1/customers/${custId}`,
        contentType: 'application/json',
        success: function (response) {
          console.log(response);
          row.remove();
        },
        error: function (xhr, status, error) {
          // Display Error Message
          console.error('Error deleting customer:', error);
        }
      });
    }
  });
});
