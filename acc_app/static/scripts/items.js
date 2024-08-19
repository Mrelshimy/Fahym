$(document).ready(() => {
  $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/items`,
    contentType: 'application/json',
    success: function (response) {
      items = response;
      if (items.length === 0) { // Check for empty array
        console.log('No items found!');
        const emptyRow = `
            <tr>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
            </tr>`;
        $('.items-table tbody').append(emptyRow);
      } else {
        console.log('Items retrieved successfully:', response);
        response.forEach(item => {
          const row = `
              <tr data-id="${item.id}">
                  <td>${item.name}</td>
                  <td>${item.code}</td>
                  <td>${item.unit}</td>
                  <td>${item.stock}</td>
                  <td>${item.purchase_price}</td>
                  <td>${item.sales_price}</td>
                  <td><a href="#" class="delete-item">Delete</a></td>
              </tr>`;
          $('.items-table tbody').append(row);
        });
      }
    },
    error: function (xhr, status, error) {
      // Display Error Message
      console.error('Error getting items:', error);
    }
  });

  $('.items-table tbody').on('click', '.delete-item', function (event) {
    event.preventDefault();
    if (confirm('Are you sure you want to delete this item?')) {
      const row = $(this).closest('tr');
      const itemId = row.data('id'); // Get the item ID from the data attribute
      console.log('Deleting item ID:', itemId);

      $.ajax({
        method: 'DELETE',
        url: `http://localhost:5001/acc_app/api/v1/items/${itemId}`,
        contentType: 'application/json',
        success: function (response) {
          console.log(response);
          row.remove();
        },
        error: function (xhr, status, error) {
          // Display Error Message
          console.error('Error deleting item:', error);
        }
      });
    }
  });
});
