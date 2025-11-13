function selectDelivery(type) {
  const deliveryBtn = document.getElementById('delivery-btn');
  const pickupBtn = document.getElementById('pickup-btn');
  const deliveryDetails = document.getElementById('delivery-details');
  const pickupDetails = document.getElementById('pickup-details');
  const shippingCostLabel = document.getElementById('shipping-cost-label');
  const shippingCostValue = document.getElementById('shipping-cost-value');

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


