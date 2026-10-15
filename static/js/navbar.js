const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navbar-menu');
if (hamburger && navMenu) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
  });
}