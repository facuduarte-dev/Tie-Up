<?php

session_start();

require_once "db_connect.php";




//Este archivo fue llamado mediante el metodo post
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $email = trim($_POST["email"] ?? "");
    $password = $_POST["password"] ?? "";

    //Si el correo electronico no tiene un formato valido
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $mensaje = "El correo electronico no es valido";
        header("Location: ../html/login.html?error=" . urlencode($mensaje));
        exit();
    }

    //Si la contraseña esta vacia
    if ($password === "") {
        $mensaje = "La contraseña es obligatoria";
        header("Location: ../html/login.html?error=" . urlencode($mensaje));
        exit();
    }

    $sql = "SELECT id_user, name, email, password
            FROM usuarios
            WHERE email = ?";


    $stmt = $conn->prepare($sql);

    if (!$stmt) {
        die("No se pudo preparar la consulta");
    }

    //Le asignamos el mail con su tipo a la consulta "$sql" original
    $stmt->bind_param("s", $email);

    $stmt->execute();

    //Guardamos el resultado de la consulta en una variable lalmada "$resultado"
    $resultado = $stmt->get_result();

    if ($resultado->num_rows !== 1) {
        $mensaje = "Correo o contraseña incorrectos";
        header("Location: ../html/login.html?error=" . urlencode($mensaje));
        exit();
    }


    $usuario = $resultado->fetch_assoc();

    if (!password_verify($password, $usuario["password"])) {
        $mensaje = "Correo o contraseña incorrectos";
        header("Location: ../html/login.html?error=" . urlencode($mensaje));
        exit();
    }


    session_regenerate_id(true);

    $_SESSION["user_id"] = $usuario["id_user"];
    $_SESSION["user_name"] = $usuario["name"];
    $_SESSION["user_email"] = $usuario["email"];

    header("Location: ../html/mi-cuenta.php");
    exit();
}

header("Location: ../html/login.html");
exit();
