(function () {
  const storageKey = "lang";
  const sourceLanguage = "es";
  let translations = {};
  let currentLanguage = localStorage.getItem(storageKey) || sourceLanguage;

  const translationsUrl = new URL(
    "../lang/translations.json",
    document.currentScript.src
  );

  function translateElement(element) {
    const instruction = element.dataset.i18n;
    if (!instruction) return;

    const separator = instruction.indexOf(":");
    const attribute = separator === -1 ? null : instruction.slice(0, separator);
    const key = separator === -1 ? instruction : instruction.slice(separator + 1);
    const dictionary = translations[currentLanguage] || {};
    const translatedText = dictionary[key];

    if (translatedText === undefined) return;

    if (attribute) {
      element.setAttribute(attribute, translatedText);
    } else {
      element.textContent = translatedText;
    }
  }

  function applyTranslations() {
    document.documentElement.lang = currentLanguage;
    document.querySelectorAll("[data-i18n]").forEach(translateElement);

    const button = document.querySelector("#language-toggle");
    if (button) {
      button.textContent = currentLanguage === "es" ? "EN" : "ES";
      button.title = currentLanguage === "es"
        ? "Cambiar a inglés"
        : "Switch to Spanish";
    }
  }

  function toggleLanguage() {
    currentLanguage = currentLanguage === "es" ? "en" : "es";
    localStorage.setItem(storageKey, currentLanguage);
    applyTranslations();
  }

  function addLanguageButton() {
    if (document.querySelector("#language-toggle")) return;

    const target = document.querySelector(".navSession") || document.querySelector("nav");
    if (!target) return;

    const button = document.createElement("button");
    button.id = "language-toggle";
    button.type = "button";
    button.addEventListener("click", toggleLanguage);
    target.appendChild(button);
  }

  document.addEventListener("DOMContentLoaded", async () => {
    try {
      const response = await fetch(translationsUrl);
      if (!response.ok) throw new Error("No se pudo cargar el archivo de idiomas");

      translations = await response.json();
      if (!translations[currentLanguage]) currentLanguage = sourceLanguage;

      addLanguageButton();
      applyTranslations();
    } catch (error) {
      console.error("No se pudieron cargar las traducciones:", error);
      localStorage.removeItem(storageKey);
    }
  });
})();
