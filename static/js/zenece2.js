document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('.z2-nav a');
  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.forEach((item) => item.classList.remove('active'));
      link.classList.add('active');
    });
  });
});
