<?php

require_once "db_connect.php";

function redirectToRegister(string $message, string $type = "register_error"): void
{
    header("Location: ../html/login.html?" . $type . "=" . urlencode($message));
    exit();
}

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: ../html/login.html");
    exit();
}

$name = trim($_POST["name"] ?? "");
$email = trim($_POST["email"] ?? "");
$password = $_POST["password"] ?? "";

if ($name === "") {
    redirectToRegister("El nombre completo es obligatorio");
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    redirectToRegister("El correo electrónico no es válido");
}

if (strlen($password) < 8 || strlen($password) > 12) {
    redirectToRegister("La contraseña debe tener entre 8 y 12 caracteres");
}

if (!preg_match("/[A-Z]/", $password)) {
    redirectToRegister("La contraseña debe contener al menos una letra mayúscula");
}

if (!preg_match("/[a-z]/", $password)) {
    redirectToRegister("La contraseña debe contener al menos una letra minúscula");
}

if (!preg_match("/[0-9]/", $password)) {
    redirectToRegister("La contraseña debe contener al menos un número");
}

if (!preg_match('/[!@#$%^&*]/', $password)) {
    redirectToRegister("La contraseña debe contener al menos un carácter especial");
}

$checkSql = "SELECT id_user FROM usuarios WHERE email = ?";
$checkStmt = $conn->prepare($checkSql);

if (!$checkStmt) {
    redirectToRegister("No se pudo comprobar el correo electrónico");
}

$checkStmt->bind_param("s", $email);
$checkStmt->execute();
$existingUser = $checkStmt->get_result();

if ($existingUser->num_rows > 0) {
    redirectToRegister("Ya existe una cuenta con ese correo electrónico");
}

$passwordHash = password_hash($password, PASSWORD_DEFAULT);
$sql = "INSERT INTO usuarios (name, email, password) VALUES (?, ?, ?)";
$stmt = $conn->prepare($sql);

if (!$stmt) {
    redirectToRegister("No se pudo preparar el registro");
}

$stmt->bind_param("sss", $name, $email, $passwordHash);

try {
    $registered = $stmt->execute();
} catch (mysqli_sql_exception $error) {
    redirectToRegister("No se pudo completar el registro");
}

if (!$registered) {
    redirectToRegister("No se pudo completar el registro");
}

redirectToRegister("La cuenta fue creada correctamente", "register_success");
