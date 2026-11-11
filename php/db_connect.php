<?php

$credentials = parse_ini_file("/var/www/facu_fx/.db_credentials.txt");

$conn = new mysqli(
    $credentials["Host"],
    $credentials["Usuario"],
    $credentials["Contraseña"],
    $credentials["BaseDeDatos"]
);

$conn->set_charset("utf8mb4");
