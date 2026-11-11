<?php

$credentials = parse_ini_file("/var/www/facu_fx/.db_credentials.txt");


$conn = new mysqli(
    $credentials["Host"],
    $credentials["Usuario"],
    $credentials["Contraseña"],
    $credentials["basesdedatos"]
);

// Verificar si la conexión falló
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

$conn->set_charset("utf8mb4");
