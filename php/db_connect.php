<?php

$host = "127.0.0.1";
$usuario = "facu_fx";
$contrasena = "5811FacuITSP#"; // Contraseña de tu usuario de MySQL
$baseDeDatos = "db_facu_fx";
$puerto = 3306;

$conn = new mysqli(
    $host,
    $usuario,
    $contrasena,
    $baseDeDatos,
    $puerto
);

if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

$conn->set_charset("utf8mb4");
