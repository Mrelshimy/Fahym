$(document).ready(function () {
  let itemOptions = '';

  $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/customers`,
    contentType: 'application/json',
    success: function (response) {
      console.log('Customers:', response);
      response.forEach(function (customer) {
        $('.customer').append(
            `<option value="${customer.name}">${customer.name}</option>`
        );
      });
    },
    error: function (xhr, status, error) {
      console.error('Error adding customers:', error);
    }
  });

  $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/items`,
    contentType: 'application/json',
    success: function (response) {
      console.log('Items:', response);
      response.forEach(function (item) {
        itemOptions += `<option value="${item.code}">${item.code} - ${item.name}</option>`;
      });
      $('main .item').append(itemOptions);
    },
    error: function (xhr, status, error) {
      console.error('Error adding items:', error);
    }
  });

  $('#add-item').click(function () {
    $('.items-table tbody').append(
        `<tr>
          <td><select type="text" class="item">${itemOptions}</td>
          <td><input type="number" class="quantity"></td>
          <td><input type="number" class="price"></td>
          <td><input type="number" class="total" disabled></td>
          <td><a href="#" class="delete-item">Delete</a></td>
        </tr>`
    );
  });

  $('.items-table tbody').on('input', '.quantity, .price', function () {
    const row = $(this).closest('tr');
    const quantity = row.find('.quantity').val();
    const price = row.find('.price').val();
    const total = quantity * price;
    row.find('.total').val(total);
    calculateInvoiceTotal();
  });

  $('.items-table tbody').on('click', '.delete-item', function (event) {
    event.preventDefault();
    const row = $(this).closest('tr');
    if (!row.hasClass('static-row')) {
      row.remove();
      calculateInvoiceTotal();
    }
  });

  $('.shipping-cost').on('input', function () {
    calculateInvoiceTotal();
  });

  function calculateInvoiceTotal () {
    let total = 0;
    $('.items-table tbody tr').each(function () {
      const rowTotal = parseFloat($(this).find('.total').val()) || 0;
      total += rowTotal;
    });
    shipping_cost = $('.shipping-cost').val();
    total += parseFloat(shipping_cost) || 0;
    $('#invoice-total').val(total);
  }

  $('#submit-btn').click(function (e) {
    e.preventDefault();

    const invoiceData = {
      code: $('.code').val(),
      customer: $('.customer').val(),
      total_price: $('#invoice-total').val(),
      date: $('.date').val(),
      shipping_cost: $('.shipping-cost').val(),
      items: []
    };

    $('.items-table tbody tr').each(function () {
      const item = $(this).find('.item').val();
      const quantity = $(this).find('.quantity').val();
      const price = $(this).find('.price').val();
      const total = $(this).find('.total').val();
      if (item && quantity && price) {
        invoiceData.items.push({
          item,
          quantity,
          price,
          total
        });
      }
    });

    $.ajax({
      method: 'POST',
      url: `http://localhost:5001/acc_app/api/v1/users/${userId}/sales_invoices`,
      contentType: 'application/json',
      data: JSON.stringify(invoiceData),
      success: function (response) {
        console.log('Invoice added successfully:', response);
        $('.add-invoice form')[0].reset();
        alert('Invoice added successfully');
      },
      error: function (xhr, status, error) {
        console.error('Error adding invoice:', error);
      }
    });
  });
});
