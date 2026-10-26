<?php

$host = getenv("DB_HOST") ?: "localhost";
$usuario = getenv("DB_USER") ?: "root";
$contrasena = getenv("DB_PASSWORD") ?: "";
$baseDeDatos = getenv("DB_NAME") ?: "TieUp";
$puerto = (int) (getenv("DB_PORT") ?: 3306);

$credentialsPath = dirname(__DIR__, 3) . "/.db_credentials.txt";

if (is_readable($credentialsPath)) {
    $credentials = [];

    foreach (file($credentialsPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        [$key, $value] = array_pad(explode(":", $line, 2), 2, "");
        $credentials[trim($key)] = trim($value);
    }

    $host = $credentials["Host"] ?? $host;
    $usuario = $credentials["Usuario"] ?? $usuario;
    $contrasena = $credentials["Contraseña"] ?? $contrasena;
    $baseDeDatos = $credentials["Base de datos"] ?? $baseDeDatos;
}

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
