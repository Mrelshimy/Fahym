$(document).ready(function () {
  let expenses = 0;
  let revenue = 0;
  let customers = [];
  let suppliers = [];

  const customersRequest = $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/customers`,
    contentType: 'application/json'
  });

  const suppliersRequest = $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/suppliers`,
    contentType: 'application/json'
  });

  const salesInvoicesRequest = $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/sales_invoices`,
    contentType: 'application/json'
  });

  const purchaseInvoicesRequest = $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/purchase_invoices`,
    contentType: 'application/json'
  });

  const itemsRequest = $.ajax({
    method: 'GET',
    url: `http://localhost:5001/acc_app/api/v1/users/${userId}/items`,
    contentType: 'application/json'
  });

  // let salesItemsRequest = $.ajax({
  //       method: 'GET',
  //       url: `http://localhost:5001/acc_app/api/v1/users/${userId}/sales_items`,
  //       contentType: 'application/json'
  // });

  $.when(customersRequest, suppliersRequest, salesInvoicesRequest, purchaseInvoicesRequest, itemsRequest /* salesItemsRequest */)
    .done(function (customersResponse, suppliersResponse, salesInvoicesResponse, purchaseInvoicesResponse, itemsResponse, salesItemsResponse) {
      customers = customersResponse[0];
      suppliers = suppliersResponse[0];
      const salesInvoices = salesInvoicesResponse[0];
      const purchaseInvoices = purchaseInvoicesResponse[0];
      const items = itemsResponse[0];
      // let salesItems = salesItemsResponse[0];

      salesInvoices.forEach(invoice => {
        revenue += invoice.total_price;
      });

      const customer_sales = {};
      salesInvoices.forEach(invoice => {
        if (customer_sales[invoice.customer_id]) {
          customer_sales[invoice.customer_id] += invoice.total_price;
        } else {
          customer_sales[invoice.customer_id] = invoice.total_price;
        }
      });

      const topCustomer = Object.keys(customer_sales).reduce((a, b) => customer_sales[a] > customer_sales[b] ? a : b);
      const topCustomerObj = customers.find(customer => customer.id === topCustomer);
      const topCustomerName = topCustomerObj ? topCustomerObj.name : 'Unknown';
      const topCustomerSalesRatio = customer_sales[topCustomer] / revenue;
      $('#top-customer').text(topCustomerName);
      $('#top-customer + h5.success').text(`${(topCustomerSalesRatio * 100).toFixed(0)}%`);

      purchaseInvoices.forEach(invoice => {
        expenses += invoice.total_price;
      });

      const supplier_sales = {};
      purchaseInvoices.forEach(invoice => {
        if (supplier_sales[invoice.supplier_id]) {
          supplier_sales[invoice.supplier_id] += invoice.total_price;
        } else {
          supplier_sales[invoice.supplier_id] = invoice.total_price;
        }
      });

      const topSupplier = Object.keys(supplier_sales).reduce((a, b) => supplier_sales[a] > supplier_sales[b] ? a : b);
      const topSupplierObj = suppliers.find(supplier => supplier.id === topSupplier);
      const topSupplierName = topSupplierObj ? topSupplierObj.name : 'Unknown';
      const topSupplierSalesRatio = supplier_sales[topSupplier] / expenses;
      $('#top-supplier').text(topSupplierName);
      $('#top-supplier + h5.success').text(`${(topSupplierSalesRatio * 100).toFixed(0)}%`);

      // let item_sales = {};
      // salesItems.forEach(item => {
      //   if (item_sales[item.item_id]) {
      //   item_sales[item.item_id] += (item.item_quantity * item.item_price);
      //   } else {
      //   item_sales[item.item_id] = (item.item_quantity * item.item_price);
      //   }
      // });

      // let topItem = Object.keys(item_sales).reduce((a, b) => item_sales[a] > item_sales[b] ? a : b);
      // let topItemObj = items.find(supplier => supplier.id === topSupplier);
      // let topItemCode = topItemObj ? topItemObj.code : "Unknown";
      // let topItemSalesRatio = item_sales[topItem] / revenue;
      // $('#top-item').text(topItemCode);
      // $('#top-item + h5.success').text(`${(topItemSalesRatio * 100).toFixed(0)}%`);
    })
    .fail(function (xhr, status, error) {
      console.error('Error in one of the requests:', error);
    });
});
