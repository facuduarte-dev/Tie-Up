(function () {
  const pagePath = window.location.pathname;
  const basePath = pagePath.includes("/html/") ? "../lang/" : "lang/";
  const storageKey = "tieup-language";
  const sourceLanguage = "es";
  let currentLanguage = localStorage.getItem(storageKey) || sourceLanguage;

  function translateNode(node, dictionary) {
    if (node.nodeType === Node.TEXT_NODE) {
      const original = node.nodeValue;
      const normalized = original.replace(/\s+/g, " ").trim();
      if (normalized && dictionary[normalized]) {
        const leading = original.match(/^\s*/)[0];
        const trailing = original.match(/\s*$/)[0];
        node.nodeValue = leading + dictionary[normalized] + trailing;
      }
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE || node.matches("script, style, textarea")) return;
    if (node.placeholder && dictionary[node.placeholder]) node.placeholder = dictionary[node.placeholder];
    if (node.title && dictionary[node.title]) node.title = dictionary[node.title];
    if (node.getAttribute("aria-label") && dictionary[node.getAttribute("aria-label")]) {
      node.setAttribute("aria-label", dictionary[node.getAttribute("aria-label")]);
    }
    node.childNodes.forEach((child) => translateNode(child, dictionary));
  }

  async function loadLanguage(language) {
    const response = await fetch(`${basePath}${language}.json`);
    if (!response.ok) throw new Error("No se pudo cargar el idioma");
    const dictionary = await response.json();
    translateNode(document.body, dictionary);
    if (dictionary[document.title]) document.title = dictionary[document.title];
    document.documentElement.lang = language;
    localStorage.setItem(storageKey, language);
    const button = document.querySelector("#language-toggle");
    if (button) button.textContent = language === "es" ? "EN" : "ES";
  }

  function addLanguageButton() {
    if (document.querySelector("#language-toggle")) return;
    const target = document.querySelector(".navSession") || document.querySelector("nav");
    if (!target) return;
    const button = document.createElement("button");
    button.id = "language-toggle";
    button.type = "button";
    button.title = "Cambio de idioma";
    button.textContent = currentLanguage === "es" ? "EN" : "ES";
    button.addEventListener("click", () => {
      currentLanguage = currentLanguage === "es" ? "en" : "es";
      localStorage.setItem(storageKey, currentLanguage);
      window.location.reload();
    });
    target.appendChild(button);
  }

  document.addEventListener("DOMContentLoaded", async () => {
    addLanguageButton();
    if (currentLanguage !== sourceLanguage) {
      try { await loadLanguage(currentLanguage); }
      catch (error) { localStorage.removeItem(storageKey); }
    }
  });
})();
