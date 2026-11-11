<?php

$credentials = parse_ini_file("/ruta/.db_credentials.txt");

$conn = new mysqli(
    $credentials["Host"],
    $credentials["Usuario"],
    $credentials["Contraseña"],
    $credentials["Base de datos"]
);

$conn->set_charset("utf8mb4");
