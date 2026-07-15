// Highlight active nav link based on current path
document.querySelectorAll(".nav-link").forEach(link => {
  if (link.href === window.location.href) link.classList.add("active");
});
