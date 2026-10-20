Saber el total de usuarios registrados:

SELECT COUNT(*) AS total_usuarios FROM usuarios;

Contar usuarios cuyo correo sea de un dominio específico (ejemplo, Gmail):

SELECT COUNT(*) AS usuarios_gmail
FROM usuarios
WHERE
    email LIKE '%@gmail.com';

Obtener la fecha del primer registro (usuario más antiguo con MIN):

SELECT MIN(created_at) AS primer_registro FROM usuarios;

Obtener la fecha del último registro (usuario más reciente con MAX):

SELECT MAX(created_at) AS ultimo_registro FROM usuarios;

Calcular el promedio de una columna numérica (ejemplo hipotético
 si agregaras una columna edad para usar AVG):

SELECT AVG(edad) AS edad_promedio FROM usuarios;

Obtener el valor mínimo y máximo de una columna numérica hipotética (edad):

SELECT MIN(edad) AS edad_minima, MAX(edad) AS edad_maxima
FROM usuarios;

Contar la cantidad de registros agrupados por fecha de creación:

SELECT
    DATE(created_at) AS fecha_registro,
    COUNT(*) AS total_registros
FROM usuarios
GROUP BY
    DATE(created_at);
