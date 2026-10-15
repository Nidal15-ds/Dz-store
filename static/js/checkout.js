function renderCheckout() {
  const cart = getCart();
  const itemsBox = document.getElementById('checkout-items');
  const hidden = document.getElementById('checkout-hidden');
  if (!itemsBox || !hidden) return;

  itemsBox.innerHTML = '';
  hidden.innerHTML = '';

  if (cart.length === 0) {
    itemsBox.innerHTML = '<p>Your cart is empty.</p>';
    return;
  }

  let total = 0;
  cart.forEach((item) => {
    total += item.price * item.quantity;

    const row = document.createElement('div');
    row.className = 'summary-row';
    row.innerHTML = `<span>${item.name} × ${item.quantity}</span><span>${(item.price * item.quantity).toLocaleString()} DZD</span>`;
    itemsBox.appendChild(row);

    const pid = document.createElement('input');
    pid.type = 'hidden';
    pid.name = 'product_id';
    pid.value = item.id;
    hidden.appendChild(pid);

    const qty = document.createElement('input');
    qty.type = 'hidden';
    qty.name = 'quantity';
    qty.value = item.quantity;
    hidden.appendChild(qty);
  });

  document.getElementById('checkout-total').textContent = total.toLocaleString() + ' DZD';
}

const checkoutForm = document.getElementById('checkout-form');
if (checkoutForm) {
  checkoutForm.addEventListener('submit', (e) => {
    if (getCart().length === 0) {
      e.preventDefault();
      alert('Your cart is empty.');
    }
  });
}

renderCheckout();