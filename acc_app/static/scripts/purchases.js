$(document).ready(() => {
  $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/suppliers`,
    contentType: 'application/json',
    success: function (response) {
      suppliers = response;
    },
    error: function (xhr, status, error) {
      // Display Error Message
      console.error('Error getting suppliers:', error);
    }
  });
  $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/purchase_invoices`,
    contentType: 'application/json',
    success: function (response) {
      invoices = response;
      if (invoices.length === 0) { // Check for empty array
        console.log('No invoices found!');
        const emptyRow = `
            <tr>
                <td>-</td>
                <td>-</td>
                <td>-</td>
                <td>-</td>
            </tr>`;
        $('.items-table tbody').append(emptyRow);
      } else {
        console.log('Invoices retrieved successfully:', response);
        response.forEach(invoice => {
          supplier = suppliers.find(supplier => supplier.id === invoice.supplier_id).name;
          const formattedDate = new Date(invoice.date).toLocaleDateString('en-US', {
            weekday: 'long', // Day of the week
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          });
          invoice.date = formattedDate;
          const row = `
              <tr data-id="${invoice.id}">
                  <td>${invoice.code}</td>
                  <td>${supplier}</td>
                  <td>${invoice.date}</td>
                  <td>${invoice.total_price}</td>
                  <td><a href="#" class="delete-item">Delete</a></td>
              </tr>`;
          $('.items-table tbody').append(row);
        });
      }
    },
    error: function (xhr, status, error) {
      // Display Error Message
      console.error('Error getting invoices:', error);
    }
  });

  $('.items-table tbody').on('click', '.delete-item', function (event) {
    event.preventDefault();
    if (confirm('Are you sure you want to delete this invoice?')) {
      const row = $(this).closest('tr');
      const invId = row.data('id'); // Get the item ID from the data attribute
      console.log('Deleting invoice ID:', invId);

      $.ajax({
        method: 'DELETE',
        url: `http://localhost:5001/acc_app/api/v1/purchase_invoices/${invId}`,
        contentType: 'application/json',
        success: function (response) {
          console.log(response);
          row.remove();
        },
        error: function (xhr, status, error) {
          // Display Error Message
          console.error('Error deleting invoice:', error);
        }
      });
    }
  });
});
