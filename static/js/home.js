document.querySelectorAll('.faq-question').forEach((btn) => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const icon = btn.querySelector('.faq-icon');
    item.classList.toggle('open');
    icon.textContent = item.classList.contains('open') ? '-' : '+';
  });
});

const suggestionForm = document.getElementById('suggestion-form');
if (suggestionForm) {
  suggestionForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const alertBox = document.getElementById('suggestion-success');
    alertBox.style.display = 'block';
    suggestionForm.reset();
    setTimeout(() => { alertBox.style.display = 'none'; }, 5000);
  });
}