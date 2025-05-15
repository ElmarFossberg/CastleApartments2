const navLinks = document.querySelectorAll('.nav-links a');
const currentPath = window.location.pathname.replace(/\/$/, ''); // remove trailing slash

navLinks.forEach(link => {
  const linkPath = link.getAttribute('href').replace(/\/$/, ''); // remove trailing slash
  if (linkPath === currentPath) {
    link.setAttribute('aria-current', 'page');
  } else {
    link.removeAttribute('aria-current');
  }
});
