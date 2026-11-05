//when the DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  //Execute this :

  //create a °variable° to locate the div with the "feedback" Id
  const feedback = document.getElementById("feedback-login");
  const registerFeedback = document.getElementById("feedback-register");

  //window.location.search devuelve la parte de la URL que comienza con ?.
  const parametros = new URLSearchParams(window.location.search);

  if (parametros.has("error")) {
    feedback.textContent = parametros.get("error");
    feedback.classList.add("error");
  } else if (parametros.has("success")) {
    feedback.textContent = parametros.get("success");
    feedback.classList.add("success");
  }

  if (parametros.has("register_error")) {
    registerFeedback.textContent = parametros.get("register_error");
    registerFeedback.classList.add("error");
  } else if (parametros.has("register_success")) {
    registerFeedback.textContent = parametros.get("register_success");
    registerFeedback.classList.add("success");
  }
});
