function getCart() {
  try {
    return JSON.parse(localStorage.getItem('dz_cart')) || [];
  } catch (e) {
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem('dz_cart', JSON.stringify(cart));
}

function updateBadge() {
  const badge = document.getElementById('cart-badge');
  if (!badge) return;
  const total = getCart().reduce((sum, item) => sum + item.quantity, 0);
  badge.textContent = total;
  badge.style.display = total > 0 ? 'inline-block' : 'none';
}

document.addEventListener('click', (e) => {
  const btn = e.target.closest('.add-btn');
  if (!btn || btn.disabled) return;
  const cart = getCart();
  const existing = cart.find((item) => item.id === parseInt(btn.dataset.id));
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({
      id: parseInt(btn.dataset.id),
      name: btn.dataset.name,
      price: parseFloat(btn.dataset.price),
      image: btn.dataset.image,
      quantity: 1,
    });
  }
  saveCart(cart);
  updateBadge();
});

updateBadge();