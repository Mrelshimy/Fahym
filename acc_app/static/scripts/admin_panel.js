$(document).ready(function () {
  let expenses = 0;
  let revenue = 0;
  let profit = 0;

  const sideMenu = document.querySelector('.container aside');
  const menuBtn = document.querySelector('#menu-btn');
  const closeBtn = document.querySelector('#close-btn');

  menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
  });

  closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
  });

  let customers = [];
  let suppliers = [];
  const invoices = [];

  // Function to fetch data using AJAX
  function fetchData (url) {
    return $.ajax({
      method: 'GET',
      url: `http://localhost:5001/acc_app/api/v1/${url}`,
      contentType: 'application/json'
    });
  }

  // Fetch all necessary data
  Promise.all([
    fetchData(`users/${userId}/customers`),
    fetchData(`users/${userId}/suppliers`),
    fetchData(`users/${userId}/sales_invoices`),
    fetchData(`users/${userId}/purchase_invoices`),
    fetchData(`users/${userId}/initial_investment`)
  ]).then(function (responses) {
    customers = responses[0];
    suppliers = responses[1];
    const salesInvoices = responses[2];
    const purchaseInvoices = responses[3];
    const initialInvestment = responses[4];

    // Process sales invoices
    if (salesInvoices.length === 0) {
      console.log('No invoices found!');
      const emptyRow = `
          <tr>
              <td>-</td>
              <td>-</td>
              <td>-</td>
              <td>-</td>
          </tr>`;
      $('.recent-orders tbody').append(emptyRow);
    } else {
      salesInvoices.slice(0, 5).forEach(invoice => {
        const customer = customers.find(customer => customer.id === invoice.customer_id).name;
        const formattedDate = new Date(invoice.date).toLocaleDateString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
        const row = `
            <tr data-id="${invoice.id}">
                <td>${invoice.code}</td>
                <td>${customer}</td>
                <td>${invoice.total_price}</td>
                <td>${formattedDate}</td>
                <td><a href="#" class="delete-item">View</a></td>
            </tr>`;
        $('.recent-orders tbody').append(row);
      });
    }

    salesInvoices.forEach(invoice => {
      revenue += invoice.total_price;
    });
    $('.sales .middle .left h1').text(revenue);

    // Process purchase invoices
    purchaseInvoices.forEach(invoice => {
      expenses += invoice.total_price;
    });
    $('.expenses .middle .left h1').text(expenses);

    // Set initial investment
    $('.investment .middle .left h1').text(initialInvestment.amount);

    // Cash on hand calculations
    const cashOnHand = initialInvestment.amount + revenue - expenses;
    $('.cash .middle .left h1').text(cashOnHand);

    // Update profit and ROI
    updateProfit();
    updateROI(initialInvestment.amount);
  }).catch(function (error) {
    console.error('Error fetching data:', error);
  });

  function updateProfit () {
    profit = revenue - expenses;
    $('.income .middle .left h1').text(profit);
    const profitRatio = profit / revenue;
    const profitPercentage = (profitRatio * 100).toFixed(0) + '%';
    $('main .insights .income .progress p').text(profitPercentage);

    const expensesRatio = expenses / revenue;
    const expensesPercentage = (expensesRatio * 100).toFixed(0) + '%';
    $('main .insights .expenses .progress p').text(expensesPercentage);

    // Calculate stroke-dasharray and stroke-dashoffset based on the profit ratio
    const expensesCircleCircumference = 2 * Math.PI * 35; // assuming the radius is 35
    const expensesDashArray = expensesCircleCircumference;
    const expensesDashOffset = expensesCircleCircumference * (1 - expensesRatio);

    // Update the circle's stroke-dasharray and stroke-dashoffset for expenses
    $('main .insights .expenses svg circle').css({
      'stroke-dasharray': expensesDashArray,
      'stroke-dashoffset': expensesDashOffset
    });

    // Calculate stroke-dasharray and stroke-dashoffset based on the profit ratio
    const circleCircumference = 2 * Math.PI * 35; // assuming the radius is 35
    const dashArray = circleCircumference;
    const dashOffset = circleCircumference * (1 - profitRatio);

    // Update the circle's stroke-dasharray and stroke-dashoffset for profit
    $('main .insights .income svg circle').css({
      'stroke-dasharray': dashArray,
      'stroke-dashoffset': dashOffset
    });
  }

  function updateROI (initialInvestmentAmount) {
    const roi = (profit / initialInvestmentAmount) * 100;
    $('.roi .middle .left h1').text(`${roi.toFixed(2)} %`);
    $('main .insights .roi .progress p').text(`${roi.toFixed(0)} %`);

    // Calculate stroke-dasharray and stroke-dashoffset based on the ROI value
    const circleCircumference = 2 * Math.PI * 35; // assuming the radius is 35
    const dashArray = circleCircumference;
    const roiRatio = roi / 100;
    const dashOffset = circleCircumference * (1 - roiRatio);

    // Update the circle's stroke-dasharray and stroke-dashoffset
    $('main .insights .roi svg circle').css({
      'stroke-dasharray': dashArray,
      'stroke-dashoffset': dashOffset
    });
  }
});
