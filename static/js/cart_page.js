
function renderCart() {
  const cart = getCart();
  const empty = document.getElementById('cart-empty');
  const full = document.getElementById('cart-full');
  const list = document.getElementById('cart-items');
  if (!list) return;

  if (cart.length === 0) {
    empty.style.display = 'flex';
    full.style.display = 'none';
    return;
  }

  empty.style.display = 'none';
  full.style.display = 'block';
  list.innerHTML = '';

  let total = 0;
  cart.forEach((item) => {
    total += item.price * item.quantity;
    const card = document.createElement('div');
    card.className = 'cart-item-card';
    card.innerHTML = `
      <img src="${item.image}" alt="${item.name}" class="cart-item-img">
      <div class="cart-item-details">
        <h3 class="cart-item-title">${item.name}</h3>
        <div class="cart-item-price">${item.price} DZD</div>
        <div class="cart-item-actions">
          <div class="qty-controls">
            <button class="qty-btn" data-action="dec" data-id="${item.id}">-</button>
            <span class="qty-value">${item.quantity}</span>
            <button class="qty-btn" data-action="inc" data-id="${item.id}">+</button>
          </div>
          <button class="remove-btn" data-action="remove" data-id="${item.id}">Remove</button>
        </div>
      </div>`;
    list.appendChild(card);
  });

  const formatted = total.toLocaleString() + ' DZD';
  document.getElementById('cart-subtotal').textContent = formatted;
  document.getElementById('cart-total').textContent = formatted;
}

document.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  const id = parseInt(btn.dataset.id);
  const action = btn.dataset.action;
  let cart = getCart();
  const item = cart.find((i) => i.id === id);
  if (!item) return;
  if (action === 'inc') item.quantity += 1;
  if (action === 'dec') item.quantity = Math.max(1, item.quantity - 1);
  if (action === 'remove') cart = cart.filter((i) => i.id !== id);
  saveCart(cart);
  updateBadge();
  renderCart();
});

renderCart();