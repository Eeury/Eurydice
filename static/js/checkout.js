let selectedDeliveryType = 'delivery'; // Track the selected delivery method

function selectDelivery(type) {
  const deliveryBtn = document.getElementById('delivery-btn');
  const pickupBtn = document.getElementById('pickup-btn');
  const deliveryDetails = document.getElementById('delivery-details');
  const pickupDetails = document.getElementById('pickup-details');
  const shippingCostLabel = document.getElementById('shipping-cost-label');
  const shippingCostValue = document.getElementById('shipping-cost-value');

  selectedDeliveryType = type; // Store the selection

  if (type === 'delivery') {
    deliveryBtn.classList.add('active');
    pickupBtn.classList.remove('active');
    deliveryDetails.style.display = 'block';
    pickupDetails.style.display = 'none';
    shippingCostLabel.textContent = 'Shipping (Standard)';
    // Keep numeric as-is; server provided initial amount
  } else if (type === 'pickup') {
    pickupBtn.classList.add('active');
    deliveryBtn.classList.remove('active');
    deliveryDetails.style.display = 'none';
    pickupDetails.style.display = 'block';
    shippingCostLabel.textContent = 'Pickup (In-Store)';
    shippingCostValue.textContent = 'FREE';
  }
}

function placeOrder() {
  // Collect user details based on delivery type
  let email, phone, address;

  if (selectedDeliveryType === 'delivery') {
    const deliveryInputs = document.querySelectorAll('#delivery-details input');
    email = deliveryInputs[0].value.trim();
    address = deliveryInputs[1].value.trim();
    phone = deliveryInputs[2].value.trim();

    // Validate delivery fields
    if (!email || !address || !phone) {
      alert('Please fill in all delivery details');
      return;
    }
  } else {
    const pickupInputs = document.querySelectorAll('#pickup-details input');
    email = pickupInputs[0].value.trim();
    phone = pickupInputs[1].value.trim();
    address = 'Collecting at Shop: Eeury Flagship, 123 Green St, Metropolis, 10001';

    // Validate pickup fields
    if (!email || !phone) {
      alert('Please fill in all pickup details');
      return;
    }
  }

  // Get order details from the page
  const totalAmount = document.getElementById('total-amount').textContent.trim();

  // Build WhatsApp message
  let message = `*NEW ORDER FROM EEURY SHOP*\n\n`;
  message += `*Customer Details:*\n`;
  message += `Email: ${email}\n`;
  message += `Phone: ${phone}\n\n`;

  message += `*Delivery Method:*\n`;
  message += selectedDeliveryType === 'delivery' ? '🚚 Delivery\n' : '🏪 Collecting at Shop\n';
  message += `Address: ${address}\n\n`;

  message += `*Order Details:*\n`;
  // Include cart items if available
  if (window.cartItems && window.cartItems.length > 0) {
    window.cartItems.forEach((item, index) => {
      message += `${index + 1}. ${item.name}\n`;
      message += `   Quantity: ${item.quantity}\n`;
      message += `   Price: KSh ${item.price}\n`;
      message += `   Subtotal: KSh ${item.lineTotal}\n\n`;
    });
  } else {
    message += `Items: (See cart)\n\n`;
  }

  message += `*Total Amount:* ${totalAmount}\n`;

  // WhatsApp number
  const whatsappNumber = '254757592565';
  const whatsappURL = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;

  // Redirect to WhatsApp
  window.open(whatsappURL, '_blank');
}

// Add event listener when the page loads
document.addEventListener('DOMContentLoaded', function () {
  const placeOrderBtn = document.querySelector('.green-button');
  if (placeOrderBtn) {
    placeOrderBtn.addEventListener('click', function (e) {
      e.preventDefault();
      placeOrder();
    });
  }
});


