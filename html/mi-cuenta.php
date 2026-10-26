<?php

session_start();

if (!isset($_SESSION["user_id"])) {
  header("Location: login.html");
  exit();
}

?>

<!doctype html>
<html lang="es">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="../css/perfil.css" />
  <link rel="stylesheet" href="../css/navbar.css" />
  <title>Mi perfil</title>
</head>



<body class="page-with-navbar">
  <header class="site-header">
    <nav class="navBar">
      <div class="logo">
        <img
          src="../docs/tie-up/logo-tie-up-transparente.png"
          alt="Logo de DevConnect" />
      </div>

      <div class="navLinks">
        <ul>
          <li><a href="index.html">Inicio</a></li>
          <li><a href="index.html#servicios">Servicios</a></li>
          <li><a href="index.html#freelancers">Freelancers</a></li>
          <li><a href="index.html#resenas">Reseñas</a></li>
          <li><a href="soporte.html">Soporte</a></li>
        </ul>
      </div>

      <div class="navSession">
        <a href="../php/logout.php">Cerrar sesión</a>
      </div>
      <button class="menu-hamburguesa" type="button" aria-label="Abrir menú" aria-expanded="false">☰</button>
    </nav>
  </header>


  <section class="title">
    <h2>Mi cuenta</h2>
    <p>Analiza tus datos y tu perfil profesional</p>
  </section>

  <section class="porfile">

    <div>
      <img id="fotoPerfil" src="../src/img/clker-free-vector-images-avatar-294480.svg" alt="Foto de perfil">

      <a href="">Cambiar foto</a>
      <h2>Información personal</h2>

      <ul>
        <li><a href="mis-servicios.html">Mis Servicios</a></li>
        <li><a href="contrataciones.html">Mis Contrataciones</a></li>
        <li><a href="">Seguridad</a></li>
      </ul>

    </div>




    <div>
      <div class="form">
        <form method="POST">
          <label for="profile-name">Nombre completo</label>
          <input
            type="text"
            id="profile-name"
            name="name"
            placeholder="Ingrese su nuevo nombre"
            value="<?php echo htmlspecialchars($_SESSION["user_name"]); ?>" />

          <label for="profile-email">Correo electrónico</label>
          <input type="email"
            id="profile-email"
            name="email"
            placeholder="Ingrese su nuevo mail"
            value="<?php echo htmlspecialchars($_SESSION["user_email"]) ?>" />




          <label for="profile-specialty">Especialidad</label>
          <input id="profile-specialty" name="specialty" type="text" placeholder="Diseño web y UX/UI" />

          <label for="profile-about">Sobre mí</label>
          <input id="profile-about" name="about" type="text" placeholder="Cuenta tu especialidad y cómo puedes ayudar">


        </form>
      </div>


      <a href="">Guardar Cambios</a>
      <a href="../php/logout.php">Cerrar sesión</a>

    </div>


  </section>



  <script src="../js/navbar.js"></script>
  <script src="../js/i18n.js"></script>
</html>
