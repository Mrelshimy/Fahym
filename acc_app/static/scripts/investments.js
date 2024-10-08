$(document).ready(() => {
  $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/investments`,
    contentType: 'application/json',
    success: function (response) {
      investments = response;
      if (investments.length === 0) { // Check for empty array
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
        console.log('Items retrieved successfully:', response);
        response.forEach(investment => {
          const formattedDate = new Date(investment.date).toLocaleDateString('en-US', {
            weekday: 'long', // Day of the week
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          });
          investment.date = formattedDate;
          const row = `
              <tr data-id="${investment.id}">
                  <td>${investment.name}</td>
                  <td>${investment.date}</td>
                  <td>${investment.amount}</td>
                  <td>${investment.remarks}</td>
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
    if (confirm('Are you sure you want to delete this investment?')) {
      const row = $(this).closest('tr');
      const investmentId = row.data('id'); // Get the item ID from the data attribute
      console.log('Deleting investment ID:', investmentId);

      $.ajax({
        method: 'DELETE',
        url: `http://localhost:5001/acc_app/api/v1/investments/${investmentId}`,
        contentType: 'application/json',
        success: function (response) {
          console.log(response);
          row.remove();
        },
        error: function (xhr, status, error) {
          // Display Error Message
          console.error('Error deleting investment:', error);
        }
      });
    }
  });
  
});
