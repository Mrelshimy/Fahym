$(document).ready(() => {
  $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/suppliers`,
    contentType: 'application/json',
    success: function (response) {
      suppliers = response;
      if (suppliers.length === 0) { // Check for empty array
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
        console.log('suppliers retrieved successfully:', response);
        response.forEach(supplier => {
          const row = `
              <tr data-id="${supplier.id}">
                  <td>${supplier.name}</td>
                  <td>${supplier.code}</td>
                  <td>${supplier.email}</td>
                  <td>${supplier.phone}</td>
                  <td><a href="#" class="delete-item">Delete</a></td>
              </tr>`;
          $('.items-table tbody').append(row);
        });
      }
    },
    error: function (xhr, status, error) {
      // Display Error Message
      console.error('Error getting suppliers:', error);
    }
  });

  $('.items-table tbody').on('click', '.delete-item', function (event) {
    event.preventDefault();
    if (confirm('Are you sure you want to delete this supplier?')) {
      const row = $(this).closest('tr');
      const suppId = row.data('id'); // Get the item ID from the data attribute
      console.log('Deleting supplier ID:', suppId);

      $.ajax({
        method: 'DELETE',
        url: `http://localhost:5001/acc_app/api/v1/suppliers/${suppId}`,
        contentType: 'application/json',
        success: function (response) {
          console.log(response);
          row.remove();
        },
        error: function (xhr, status, error) {
          // Display Error Message
          console.error('Error deleting supplier:', error);
        }
      });
    }
  });
});
