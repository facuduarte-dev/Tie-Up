document.querySelectorAll(".navBar").forEach((nav) => {
  const button = nav.querySelector(".menu-hamburguesa");

  if (!button) return;

  button.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("menu-abierto");
    button.setAttribute("aria-expanded", String(isOpen));
    button.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
    button.textContent = isOpen ? "✕" : "☰";
  });

  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("menu-abierto");
      button.setAttribute("aria-expanded", "false");
      button.setAttribute("aria-label", "Abrir menú");
      button.textContent = "☰";
    });
  });
});
