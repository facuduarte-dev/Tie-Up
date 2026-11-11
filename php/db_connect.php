<?php

$credentials = parse_ini_file("/var/www/facu_fx/.db_credentials.txt");

$conn = new mysqli(
    $credentials["localhost"],
    $credentials["facu_fx"],
    $credentials["5811FacuITSP#"],
    $credentials["BaseDeDatos"]
);

$conn->set_charset("utf8mb4");
