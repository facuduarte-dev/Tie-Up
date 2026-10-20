# Guia offline: autenticacion completa en Tie-Up

## PHP, MySQL, sesiones y JavaScript, aprendidos paso a paso

Esta guia esta adaptada al proyecto ubicado en `/opt/lampp/htdocs/WebDesign` y al punto exacto alcanzado durante el acompañamiento. No esta pensada para copiar todo de una vez. Esta pensada para que puedas construir, probar, equivocarte, corregir y finalmente explicar cada parte.

---

## Como usar esta guia

En cada etapa vas a encontrar:

1. **Objetivo:** que comportamiento queremos conseguir.
2. **Por que:** para que existe esa parte del sistema.
3. **Conceptos nuevos:** vocabulario que deberias poder explicar.
4. **Tu tarea:** lo que tenes que intentar escribir vos.
5. **Prueba:** como saber si realmente funciona.
6. **Pistas:** ayuda gradual si te trabas.
7. **Solucion de referencia:** para comparar despues de intentarlo.
8. **Preguntas de defensa:** preguntas que te pueden hacer.

Regla recomendada: no mires la solucion de referencia hasta haber intentado la tarea durante al menos diez minutos.

Cuando una etapa funcione, hace un commit o guarda una copia. Asi podes volver atras si la siguiente prueba rompe algo.

---

# Parte 1. El sistema completo antes de seguir programando

## 1.1 Que estamos construyendo

El sistema permite que una persona:

1. Complete un formulario de registro.
2. Sea validada por el navegador y por PHP.
3. Quede guardada en MySQL con una contrasena protegida.
4. Inicie sesion usando correo y contrasena.
5. Reciba una sesion que la identifica en las siguientes paginas.
6. Entre a una pagina privada.
7. Cierre la sesion.
8. Vea mensajes de error o exito dentro de la interfaz.

El recorrido general es:

```text
Navegador
   |
   | formulario HTTP POST
   v
PHP
   |
   | consulta preparada
   v
MySQL
   |
   | resultado
   v
PHP crea una sesion
   |
   | redireccion HTTP
   v
Pagina privada
```

JavaScript no reemplaza a PHP. JavaScript mejora la experiencia en el navegador. PHP sigue siendo responsable de la seguridad porque el usuario puede desactivar o modificar JavaScript.

## 1.2 Responsabilidad de cada tecnologia

### HTML

Define la estructura: formularios, inputs, botones y contenedores donde se mostraran mensajes.

### CSS

Define la apariencia: colores, tamanos, posiciones, estados de error y exito.

### JavaScript

Se ejecuta en el navegador. Puede leer el HTML, responder a eventos, validar antes de enviar y mostrar mensajes sin modificar manualmente el archivo HTML.

### PHP

Se ejecuta en el servidor. Recibe formularios, valida datos, consulta MySQL, crea sesiones y decide las redirecciones.

### MySQL

Conserva los usuarios aunque cierres el navegador o reinicies la computadora.

### Sesion

Permite que PHP recuerde que varias peticiones HTTP pertenecen al mismo usuario autenticado.

## 1.3 Diferencia entre datos persistentes y datos temporales

La tabla `usuarios` es persistente. Un usuario registrado sigue existiendo manana.

`$_SESSION` es temporal. Representa el estado de una visita autenticada. Al cerrar la sesion, se elimina ese estado, pero el usuario continua en la base y puede volver a iniciar sesion.

---

# Parte 2. Estado actual de tu proyecto

Antes de continuar, tu proyecto ya tiene estas piezas:

- `sql/setup.sql`: crea la base `TieUp` y la tabla `usuarios`.
- `php/db_connect.php`: abre una conexion con MySQL usando `mysqli`.
- `php/register.php`: valida y registra usuarios.
- `php/login.php`: busca usuarios, verifica la contrasena y crea la sesion.
- `html/mi-cuenta.php`: pagina privada que comprueba la sesion.
- `html/logout.php`: elimina la sesion.
- `html/login.html`: contiene los formularios de login y registro.
- `js/script.js`: ya esta vinculado con el HTML y encuentra `#feedback`.

Tu JavaScript actual es equivalente a:

```javascript
const feedback = document.getElementById("feedback");
console.log(feedback);
```

Eso demuestra que:

1. La ruta del `<script>` es correcta.
2. El navegador ejecuta el archivo.
3. `document.getElementById` encuentra el elemento.

## 2.1 Antes de cada jornada

En Linux con XAMPP, comproba que Apache y MySQL esten activos:

```bash
sudo /opt/lampp/lampp start
sudo /opt/lampp/lampp status
```

Si `index.html` funciona pero un PHP devuelve error 500, revisa el registro:

```bash
tail -n 40 /opt/lampp/logs/error_log
```

Un HTML puede funcionar con MySQL apagado porque es estatico. Un PHP que incluye `db_connect.php` necesita que MySQL este activo.

---

# Parte 3. JavaScript desde el punto donde quedamos

## Etapa 1. Cambiar el texto de un elemento

### Objetivo

Usar la variable `feedback` para escribir un mensaje visible en la pagina.

### Concepto nuevo: objeto y propiedad

`feedback` contiene un objeto que representa un elemento HTML. Ese objeto posee propiedades. Una es `textContent`, que representa su texto interior.

La forma general de acceder a una propiedad es:

```text
objeto.propiedad
```

La asignacion utiliza `=`:

```text
objeto.propiedad = nuevoValor
```

### Tu tarea

Asigna un texto de prueba a la propiedad `textContent` de `feedback`.

### Prueba

Recarga `login.html`. El mensaje debe aparecer dentro del formulario de inicio de sesion.

Luego abre las herramientas de desarrollo, pestaña Elements o Inspector, y busca el `div`. Vas a ver que el navegador muestra texto dentro del elemento, aunque el archivo guardado siga teniendo el `div` vacio.

### Pista 1

La instruccion comienza con el nombre de la variable: `feedback`.

### Pista 2

La propiedad es `textContent`.

### Solucion de referencia

```javascript
const feedback = document.getElementById("feedback");

feedback.textContent = "Este mensaje fue agregado con JavaScript";
```

### Para explicar oralmente

> JavaScript obtiene una referencia al elemento mediante su id y modifica la propiedad `textContent`. El archivo HTML no se reescribe; cambia el DOM que el navegador mantiene en memoria.

## Etapa 2. Que es el DOM

DOM significa Document Object Model. El navegador transforma el HTML en una estructura de objetos.

Este HTML:

```html
<form>
  <div id="feedback"></div>
  <button>Entrar</button>
</form>
```

se interpreta aproximadamente como:

```text
form
|- div#feedback
`- button
```

JavaScript no trabaja directamente con el texto del archivo. Trabaja con ese arbol de objetos.

Metodos comunes:

- `getElementById`: busca un elemento por su id.
- `querySelector`: busca el primer elemento que coincida con un selector CSS.
- `querySelectorAll`: devuelve todos los que coincidan.

Ejercicio mental: explica por que un `id` no deberia repetirse. Respuesta: porque identifica de forma unica un elemento y `getElementById` espera esa unicidad.

## Etapa 3. Esperar a que el documento este listo

### Objetivo

Entender por que el material original usa `DOMContentLoaded`.

Si el `<script>` esta al final del `body`, el navegador ya leyo los elementos anteriores. Por eso tu codigo actual encuentra `feedback`.

Si el script estuviera en el `head`, podria ejecutarse antes de que exista el `div`. En ese caso `getElementById` devolveria `null`.

`DOMContentLoaded` es un evento que se dispara cuando el navegador termino de construir el DOM.

### Conceptos nuevos

- Un **evento** informa que algo ocurrio.
- Un **listener** es una funcion que espera ese evento.
- Una **funcion callback** es una funcion entregada a otra funcion para que se ejecute mas tarde.

### Tu tarea

Envolve la busqueda de `feedback` y la asignacion del mensaje dentro de un listener de `DOMContentLoaded`.

### Pistas

1. El objeto que escucha es `document`.
2. El metodo es `addEventListener`.
3. Recibe el nombre del evento y una funcion.
4. Podes usar una funcion flecha: `() => { ... }`.

### Solucion de referencia

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const feedback = document.getElementById("feedback");
  feedback.textContent = "El DOM ya esta disponible";
});
```

### Desarmando la sintaxis

```javascript
() => {
  // instrucciones
}
```

Es una funcion flecha. Los parentesis vacios indican que no recibe parametros. Las llaves contienen lo que se ejecutara.

No es obligatorio usar `DOMContentLoaded` si el script permanece al final del `body`, pero aprenderlo te permite entender el ejemplo original y mover el script sin romper la seleccion.

## Etapa 4. Leer parametros de la URL

### Objetivo

Conseguir que el mensaje no sea fijo. Debe salir de una URL como:

```text
login.html?error=Correo%20o%20contrasena%20incorrectos
```

La parte posterior a `?` se llama query string.

```text
?error=Correo incorrecto&origen=login
```

contiene dos pares clave-valor:

- clave `error`, valor `Correo incorrecto`;
- clave `origen`, valor `login`.

### Conceptos nuevos

`window` representa la ventana del navegador.

`window.location` contiene informacion sobre la URL actual.

`window.location.search` devuelve la parte que comienza con `?`.

`URLSearchParams` convierte esa cadena en un objeto facil de consultar.

### Experimento 1

Abri manualmente:

```text
http://localhost/WebDesign/html/login.html?error=Mensaje%20de%20prueba
```

En la consola escribi:

```javascript
window.location.search
```

Observa el resultado.

### Experimento 2

En `script.js`, crea una constante que guarde un nuevo `URLSearchParams` construido con `window.location.search`. Mostrala con `console.log`.

### Solucion de referencia

```javascript
const parametros = new URLSearchParams(window.location.search);
console.log(parametros);
```

`new` crea una nueva instancia del objeto. Es parecido a construir un objeto con `new` en Java.

## Etapa 5. Preguntar si existe un error

### Objetivo

Mostrar el mensaje solamente si la URL tiene el parametro `error`.

Necesitamos una decision:

```text
SI existe error
    mostrar su valor
SI NO
    dejar el contenedor vacio
```

En JavaScript se escribe con `if`:

```javascript
if (condicion) {
  // se ejecuta si la condicion es verdadera
}
```

`URLSearchParams` ofrece:

- `has("error")`: responde `true` o `false`.
- `get("error")`: obtiene el valor.

### Tu tarea

1. Elimina el mensaje fijo.
2. Pregunta si `parametros` contiene `error`.
3. Si existe, asigna su valor a `feedback.textContent`.

### Prueba

- Abri `login.html`: el contenedor debe quedar vacio.
- Abri `login.html?error=Prueba`: debe mostrar `Prueba`.
- Abri `login.html?otro=Prueba`: no debe mostrar nada.

### Solucion de referencia

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const feedback = document.getElementById("feedback");
  const parametros = new URLSearchParams(window.location.search);

  if (parametros.has("error")) {
    feedback.textContent = parametros.get("error");
  }
});
```

## Etapa 6. Diferenciar error y exito

### Objetivo

Aceptar tambien una URL como:

```text
login.html?success=Registro%20completado
```

El algoritmo sera:

```text
si hay error:
    mostrar error
si no, si hay success:
    mostrar success
```

La segunda decision se expresa con `else if`.

Ademas, queremos agregar una clase CSS sin reemplazar la clase `feedback`. Para eso existe:

```javascript
elemento.classList.add("nombre-de-clase")
```

### Tu tarea

- Si existe `error`, muestra el texto y agrega la clase `error`.
- Si no existe error pero existe `success`, muestra el texto y agrega la clase `success`.

### Solucion de referencia

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const feedback = document.getElementById("feedback");
  const parametros = new URLSearchParams(window.location.search);

  if (parametros.has("error")) {
    feedback.textContent = parametros.get("error");
    feedback.classList.add("error");
  } else if (parametros.has("success")) {
    feedback.textContent = parametros.get("success");
    feedback.classList.add("success");
  }
});
```

### CSS como ejercicio

En `css/login.css`, crea estilos para:

- `.feedback`: espacio, relleno y bordes redondeados.
- `.feedback:empty`: ocultar el contenedor cuando no tenga texto.
- `.feedback.error`: fondo y texto asociados a error.
- `.feedback.success`: fondo y texto asociados a exito.

Pista: `display: none` oculta un elemento. El selector `:empty` coincide cuando no contiene texto ni hijos.

### Solucion de referencia posible

```css
.feedback {
  padding: 12px;
  border-radius: 8px;
  font-size: 0.9rem;
}

.feedback:empty {
  display: none;
}

.feedback.error {
  color: #8a1c1c;
  background: #fde8e8;
  border: 1px solid #f3b8b8;
}

.feedback.success {
  color: #17643a;
  background: #e5f7ed;
  border: 1px solid #a8ddbd;
}
```

Los colores son una referencia. Podes adaptarlos a tu paleta.

---

# Parte 4. Conectar los mensajes con PHP

Hasta ahora escribimos manualmente la URL. Ahora PHP debe construir la redireccion cuando detecte un resultado.

## Etapa 7. Sustituir `echo` por una redireccion

### Situacion actual

En `login.php` existen respuestas similares a:

```php
echo "Correo o contrasena incorrectos";
exit();
```

Eso muestra una pagina blanca porque la respuesta de PHP contiene solamente texto.

### Objetivo

Volver a `login.html` y enviar el mensaje en la query string.

La idea general es:

```php
header("Location: ruta?error=mensaje");
exit();
```

### Por que usamos `urlencode`

Una URL no puede transportar cualquier caracter literalmente. Los espacios, tildes y otros simbolos deben codificarse.

```php
$mensaje = "Correo o contrasena incorrectos";
$mensajeSeguroParaURL = urlencode($mensaje);
```

No confundas `urlencode` con `htmlspecialchars`:

- `urlencode` prepara texto para una URL.
- `htmlspecialchars` prepara texto para insertarlo en HTML.

### Tu tarea

En el primer error de `login.php`:

1. Guarda el mensaje en una variable.
2. Redirige a `../html/login.html` agregando `?error=`.
3. Codifica el mensaje.
4. Conserva `exit()`.

### Prueba

Envia un correo con formato incorrecto. Debes volver al formulario, ver el mensaje y observar `?error=...` en la barra de direcciones.

### Solucion de referencia para un caso

```php
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $mensaje = "El correo electronico no es valido";
    header("Location: ../html/login.html?error=" . urlencode($mensaje));
    exit();
}
```

### Tu siguiente reto

Aplica el mismo patron a:

- contrasena vacia;
- usuario inexistente;
- contrasena incorrecta.

Para usuario inexistente y contrasena incorrecta usa el mismo mensaje. Esto evita revelar si un correo esta registrado.

## Etapa 8. Entender la concatenacion en PHP

En PHP, el punto concatena cadenas:

```php
"Hola " . $nombre
```

Por eso:

```php
"../html/login.html?error=" . urlencode($mensaje)
```

une la ruta fija con el mensaje codificado.

En JavaScript, normalmente se usa `+` o plantillas con backticks. No mezcles los operadores de ambos lenguajes.

## Etapa 9. Mensaje despues del registro

### Objetivo

Despues de un registro correcto, no mostrar `echo`. Volver al formulario indicando que ya puede iniciar sesion.

El flujo sera:

```text
registro correcto
-> login.html?success=Cuenta creada correctamente
-> JavaScript muestra el mensaje verde
```

### Tu tarea

En `register.php`, reemplaza el `echo` final por una redireccion que use el parametro `success`.

### Prueba

Registra un correo nuevo. Debes volver a la pagina de formularios y ver el mensaje de exito.

### Solucion de referencia

```php
$mensaje = "Cuenta creada correctamente. Ya podes iniciar sesion";
header("Location: ../html/login.html?success=" . urlencode($mensaje));
exit();
```

## Etapa 10. Dos formularios en una sola pagina

El ejemplo original tenia `login.html` y `register.html` separados. Tu proyecto tiene ambos formularios juntos. Eso genera una decision de interfaz: donde mostramos cada mensaje.

Opcion sencilla:

- un unico `#feedback` general arriba de las dos tarjetas;
- todos los mensajes aparecen alli.

Opcion mas clara:

- `#login-feedback` dentro del login;
- `#register-feedback` dentro del registro;
- PHP agrega tambien `origen=login` u `origen=registro`;
- JavaScript elige el contenedor adecuado.

Para terminar el ejercicio original, la opcion sencilla es suficiente. Como tu `#feedback` esta dentro del login, los mensajes de registro apareceran del lado izquierdo. Funciona, aunque mas adelante podes mejorar la ubicacion.

Reto opcional: agrega `origen=registro` a la URL y decide desde JavaScript que contenedor utilizar.

---

# Parte 5. Registro seguro y correo duplicado

## Etapa 11. Evitar avisos de indices inexistentes

En `login.php` ya usas:

```php
$_POST["email"] ?? ""
```

El operador `??` se llama null coalescing. Si la clave no existe, devuelve el valor de la derecha.

En `register.php`, conviene aplicar el mismo criterio a `name`, `email` y `password`.

### Tu tarea

Modifica la lectura de los tres campos para que tengan un valor alternativo vacio.

### Por que

El atributo HTML `required` ayuda al usuario, pero alguien puede enviar una peticion manual sin respetar el formulario. PHP no debe asumir que las claves existen.

### Solucion de referencia

```php
$name = trim($_POST["name"] ?? "");
$email = trim($_POST["email"] ?? "");
$password = $_POST["password"] ?? "";
```

## Etapa 12. Correo unico y errores de MySQL

La tabla declara:

```sql
email VARCHAR(150) NOT NULL UNIQUE
```

`UNIQUE` garantiza que dos usuarios no pueden compartir el mismo correo. Esa regla vive en la base y es importante aunque PHP tambien valide.

Actualmente, si repetis un correo, `$stmt->execute()` puede lanzar una excepcion y producir error 500.

Hay dos estrategias educativas:

### Estrategia A: consultar antes de insertar

1. Hacer `SELECT id_user FROM usuarios WHERE email = ?`.
2. Si existe una fila, redirigir con un error.
3. Si no existe, ejecutar el `INSERT`.

Ventaja: facil de entender.

Limitacion: entre el `SELECT` y el `INSERT`, otra peticion podria insertar el mismo correo. La restriccion `UNIQUE` sigue siendo necesaria.

### Estrategia B: intentar insertar y capturar la excepcion

Se usa `try/catch` y se interpreta el codigo de error de duplicado.

Ventaja: la base es la autoridad final.

Para tu nivel actual, implementa primero la estrategia A y conserva `UNIQUE`.

## Etapa 13. Construir la consulta de existencia

### Objetivo

Antes de calcular el hash e insertar, comprobar si el correo ya existe.

### Algoritmo, sin codigo

```text
preparar SELECT con un signo ?
vincular el correo como string
ejecutar
obtener resultado
si hay al menos una fila:
    redirigir con error
si no:
    continuar con password_hash e INSERT
```

### Tu tarea

Intenta escribirlo comparando con el `SELECT` que ya existe en `login.php`. No lo copies literalmente: identifica que partes se repiten y que columnas necesitas realmente.

### Preguntas para orientarte

1. Necesitas obtener la contrasena? No, solo saber si existe.
2. Cuantos placeholders tiene la consulta? Uno.
3. Que letra usa `bind_param` para un string? `s`.
4. Que condicion indica que existe? `num_rows > 0`.

### Solucion de referencia

```php
$sqlBuscar = "SELECT id_user FROM usuarios WHERE email = ?";
$stmtBuscar = $conn->prepare($sqlBuscar);
$stmtBuscar->bind_param("s", $email);
$stmtBuscar->execute();
$resultado = $stmtBuscar->get_result();

if ($resultado->num_rows > 0) {
    $mensaje = "Ya existe una cuenta con ese correo";
    header("Location: ../html/login.html?error=" . urlencode($mensaje));
    exit();
}
```

### Mejora posterior

Podes verificar si `prepare` devolvio `false` antes de usar `bind_param`, igual que hiciste en el login.

---

# Parte 6. Validacion de registro con JavaScript

## Etapa 14. Por que validar dos veces

Validaremos en JavaScript y en PHP.

JavaScript:

- responde inmediatamente;
- evita una peticion innecesaria;
- mejora la experiencia.

PHP:

- no puede ser evitado por el usuario;
- protege la base;
- es la validacion de seguridad real.

Nunca elimines las validaciones de PHP porque agregaste JavaScript.

## Etapa 15. Identificar el formulario de registro

Para que JavaScript encuentre solamente el formulario de registro, agrega un `id` descriptivo a ese `<form>`.

Luego, en JavaScript:

1. Busca el formulario.
2. Comprueba si fue encontrado.
3. Escucha su evento `submit`.

### Concepto: evento submit

Se dispara cuando el usuario intenta enviar el formulario, ya sea con el boton o presionando Enter.

El listener recibe un objeto evento:

```javascript
(event) => {
  // event contiene informacion sobre el envio
}
```

`event.preventDefault()` cancela temporalmente el comportamiento normal. Solo debes llamarlo cuando existe un error. Si todo es valido, no lo llamas y el formulario viaja a PHP.

## Etapa 16. Obtener los valores

Podes agregar ids a los inputs del registro y buscarlos individualmente, o usar el formulario:

```javascript
const nombre = formulario.elements.name.value;
```

Para aprender DOM, usar ids al principio es mas explicito.

No reutilices el mismo id para inputs de login y registro. Los atributos `name` pueden repetirse entre formularios; los `id` no.

Ejemplo de nombres claros:

- `register-form`;
- `register-name`;
- `register-email`;
- `register-password`;
- `register-feedback`.

## Etapa 17. Validar la contrasena por partes

Las reglas del servidor son:

- minimo 8 caracteres;
- al menos una mayuscula;
- al menos una minuscula;
- al menos un numero;
- al menos uno de `!@#$%^&*`.

En JavaScript, una expresion regular se puede probar asi:

```javascript
/[A-Z]/.test(password)
```

El resultado es booleano: `true` o `false`.

### Ejercicio en la consola

Proba:

```javascript
/[A-Z]/.test("prueba123!")
/[A-Z]/.test("Prueba123!")
```

Explica por que los resultados son diferentes.

## Etapa 18. Algoritmo de validacion

Intenta construir este comportamiento:

```text
cuando se intenta enviar el registro:
    leer nombre, email y contrasena

    si el nombre esta vacio:
        cancelar envio
        mostrar error
        terminar la funcion

    si la contrasena tiene menos de 8 caracteres:
        cancelar envio
        mostrar error
        terminar la funcion

    repetir con mayuscula, minuscula, numero y simbolo

    si todo es valido:
        no cancelar
        dejar que el navegador envie a register.php
```

El `return` termina la funcion actual. Resulta util para no continuar evaluando reglas despues de encontrar el primer error.

## Etapa 19. Solucion de referencia comentada

Esta es una referencia completa. Leela solamente despues de tu intento y adaptala a los ids que hayas elegido.

```javascript
const registerForm = document.getElementById("register-form");
const registerFeedback = document.getElementById("register-feedback");

if (registerForm) {
  registerForm.addEventListener("submit", (event) => {
    const name = document.getElementById("register-name").value.trim();
    const password = document.getElementById("register-password").value;

    if (name === "") {
      event.preventDefault();
      registerFeedback.textContent = "El nombre es obligatorio";
      registerFeedback.className = "feedback error";
      return;
    }

    if (password.length < 8) {
      event.preventDefault();
      registerFeedback.textContent = "La contrasena debe tener al menos 8 caracteres";
      registerFeedback.className = "feedback error";
      return;
    }

    if (!/[A-Z]/.test(password)) {
      event.preventDefault();
      registerFeedback.textContent = "Falta una letra mayuscula";
      registerFeedback.className = "feedback error";
      return;
    }

    if (!/[a-z]/.test(password)) {
      event.preventDefault();
      registerFeedback.textContent = "Falta una letra minuscula";
      registerFeedback.className = "feedback error";
      return;
    }

    if (!/[0-9]/.test(password)) {
      event.preventDefault();
      registerFeedback.textContent = "Falta un numero";
      registerFeedback.className = "feedback error";
      return;
    }

    if (!/[!@#$%^&*]/.test(password)) {
      event.preventDefault();
      registerFeedback.textContent = "Falta un caracter especial";
      registerFeedback.className = "feedback error";
    }
  });
}
```

### Que debes poder explicar

- Por que se comprueba `if (registerForm)`.
- Por que `preventDefault` solo aparece en errores.
- Por que usamos `.value`.
- Por que `trim` es apropiado para el nombre pero no para la contrasena.
- Que hace `.test`.
- Para que sirve `return`.

## Etapa 20. Validar correo en el navegador

Tu input usa `type="email"` y `required`. El navegador ya realiza una validacion basica antes del submit.

PHP usa `filter_var` porque no debe confiar en el navegador.

No necesitas escribir inmediatamente una expresion regular propia para correo. Las expresiones de email suelen ser faciles de hacer mal.

---

# Parte 7. Mostrar y ocultar contrasenas

Los iconos de ojo ya existen en el HTML, pero aun no tienen comportamiento.

## Etapa 21. Pensar el cambio de estado

Un input puede tener:

```html
type="password"
```

o:

```html
type="text"
```

El algoritmo es:

```text
al hacer clic en el ojo:
    si el input es password:
        cambiarlo a text
    si no:
        cambiarlo a password
```

Necesitas vincular cada icono con el input que controla. Una opcion clara es usar un atributo personalizado:

```html
data-target="login-password"
```

Los atributos `data-*` guardan informacion propia en HTML. JavaScript puede leerlos mediante `elemento.dataset.target`.

## Etapa 22. Trabajar con varios elementos

`querySelectorAll(".ojo")` devuelve todos los iconos con esa clase.

`forEach` permite ejecutar una funcion para cada icono:

```javascript
ojos.forEach((ojo) => {
  // configurar este ojo
});
```

### Tu reto

1. Agrega ids diferentes a las dos contrasenas.
2. Agrega `data-target` a cada icono.
3. Selecciona todos los iconos.
4. Para cada uno, escucha `click`.
5. Busca el input indicado por `dataset.target`.
6. Cambia su atributo `type`.

### Solucion de referencia para comparar

```javascript
const eyes = document.querySelectorAll(".ojo");

eyes.forEach((eye) => {
  eye.addEventListener("click", () => {
    const inputId = eye.dataset.target;
    const passwordInput = document.getElementById(inputId);

    if (passwordInput.type === "password") {
      passwordInput.type = "text";
    } else {
      passwordInput.type = "password";
    }
  });
});
```

Mejora opcional: alterna tambien las clases `fa-eye` y `fa-eye-slash` con `classList`.

---

# Parte 8. Sesiones explicadas en profundidad

## Etapa 23. Que ocurre al iniciar sesion

Despues de verificar la contrasena, `login.php` ejecuta:

```php
session_regenerate_id(true);
```

Esto cambia el identificador de sesion despues de autenticar. Ayuda contra ataques de fijacion de sesion.

Luego guarda:

```php
$_SESSION["user_id"] = $usuario["id_user"];
$_SESSION["user_name"] = $usuario["name"];
$_SESSION["user_email"] = $usuario["email"];
```

El navegador recibe una cookie con un identificador, normalmente `PHPSESSID`. La cookie no necesita contener el nombre ni el correo. PHP usa el identificador para recuperar los datos almacenados en el servidor.

## Etapa 24. Proteger una pagina

La proteccion de `mi-cuenta.php` sigue esta idea:

```text
iniciar/acceder a la sesion
si no existe user_id:
    volver al login
si existe:
    continuar enviando HTML
```

El bloque debe estar antes del HTML porque `header` necesita enviarse antes del cuerpo de la respuesta.

### Pregunta frecuente

**Por que comprobar `user_id` y no solamente `user_name`?**

Porque el id es la identidad primaria del registro y se crea solamente despues de autenticar. El nombre podria repetirse y puede cambiar.

## Etapa 25. Salida segura en HTML

Cuando insertas datos en un atributo HTML usas:

```php
htmlspecialchars($_SESSION["user_name"], ENT_QUOTES, "UTF-8")
```

`htmlspecialchars` evita que caracteres como `<`, `>`, `&` y comillas se interpreten como marcado.

Aunque el dato venga de tu propia sesion, originalmente fue escrito por un usuario. Por eso se escapa al mostrarlo.

## Etapa 26. Cerrar sesion

Tu logout hace:

1. `session_start()`: abre la sesion identificada por la cookie.
2. `$_SESSION = []`: vacia los datos.
3. `session_destroy()`: elimina los datos de sesion del servidor.
4. `header(...)`: vuelve al login.
5. `exit()`: termina el script.

### Mejora del ejemplo original

Podes redirigir con un mensaje de exito:

```text
login.html?success=Sesion cerrada correctamente
```

Tu JavaScript ya sabra mostrarlo.

### Mejora adicional de cookie

En proyectos mas exigentes tambien se elimina explicitamente la cookie de sesion. Para el alcance del ejercicio original, vaciar y destruir la sesion es suficiente; anota que la cookie puede quedar en el navegador sin apuntar a datos validos.

---

# Parte 9. Seguridad de contrasenas y consultas

## Etapa 27. Hash no significa cifrado reversible

`password_hash` produce un hash diseñado para contrasenas. No necesitas ni debes descifrarlo.

Registro:

```text
contrasena escrita
-> password_hash
-> hash almacenado
```

Login:

```text
contrasena escrita + hash almacenado
-> password_verify
-> true o false
```

Nunca compares:

```php
$password === $usuario["password"]
```

porque una es texto ingresado y la otra es un hash.

## Etapa 28. Consultas preparadas

Una consulta preparada separa la estructura SQL de los datos:

```sql
SELECT ... WHERE email = ?
```

El `?` es un placeholder. Despues:

```php
$stmt->bind_param("s", $email);
```

indica que el valor es string.

Esto evita construir SQL concatenando entrada del usuario y reduce el riesgo de inyeccion SQL.

Tipos comunes de `bind_param`:

- `s`: string;
- `i`: integer;
- `d`: double;
- `b`: blob.

## Etapa 29. Mensajes de autenticacion

Es preferible mostrar:

```text
Correo o contrasena incorrectos
```

para ambos casos, en lugar de informar si el correo existe. Asi no ayudas a enumerar usuarios registrados.

## Etapa 30. Errores tecnicos frente a mensajes para usuarios

Durante desarrollo, los registros del servidor pueden contener detalles tecnicos. En la interfaz, muestra mensajes comprensibles sin revelar:

- contrasenas;
- consultas completas;
- rutas internas;
- configuracion de la base;
- trazas de excepciones.

---

# Parte 10. Completar y ordenar el backend

## Etapa 31. Aceptar solamente POST

Tus scripts procesan datos dentro de:

```php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // proceso
}
```

Una mejora es decidir que hacer si alguien abre directamente `login.php` o `register.php` por GET. Podes redirigir al formulario o responder con codigo 405.

Para un proyecto educativo, una redireccion al formulario es clara.

## Etapa 32. Cerrar recursos

Al terminar puedes cerrar sentencias y conexion:

```php
$stmt->close();
$conn->close();
```

PHP normalmente libera recursos al finalizar la peticion, por lo que no es la prioridad funcional. Es una buena practica de orden y hace explicito el ciclo de vida.

No coloques cierres despues de un `exit`, porque nunca se ejecutarian. Si deseas cerrarlos, hazlo antes de redirigir.

## Etapa 33. Charset

`$conn->set_charset("utf8mb4")` permite manejar correctamente caracteres Unicode. Es preferible a confiar en valores predeterminados.

## Etapa 34. Configuracion y produccion

En tu entorno local, usuario `root` sin contrasena puede ser la configuracion predeterminada de XAMPP. No es apropiada para publicar un sitio.

En produccion deberias:

- crear un usuario de base con permisos limitados;
- usar una contrasena fuerte;
- guardar secretos fuera del repositorio;
- desactivar mensajes tecnicos visibles;
- usar HTTPS;
- configurar cookies `Secure`, `HttpOnly` y `SameSite`.

Estas mejoras exceden el ejemplo inicial, pero deberias poder mencionar la diferencia entre desarrollo local y produccion.

---

# Parte 11. Pruebas completas

No alcanza con probar solamente el camino exitoso.

## 11.1 Matriz de registro

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Nombre vacio | espacios | error, no insertar |
| Correo invalido | `abc` | error, no insertar |
| Contrasena corta | `Aa1!` | error |
| Sin mayuscula | `prueba123!` | error |
| Sin minuscula | `PRUEBA123!` | error |
| Sin numero | `PruebaABC!` | error |
| Sin simbolo | `Prueba123` | error |
| Correo repetido | correo existente | error controlado |
| Datos validos | correo nuevo | registro y mensaje de exito |

## 11.2 Matriz de login

| Caso | Resultado esperado |
|---|---|
| Correo invalido | mensaje dentro del formulario |
| Correo no registrado | mensaje generico |
| Contrasena incorrecta | mensaje generico |
| Datos correctos | redireccion a Mi cuenta |
| Abrir login.php por GET | volver al formulario |

## 11.3 Matriz de sesion

| Caso | Resultado esperado |
|---|---|
| Abrir Mi cuenta sin login | redireccion a login |
| Abrir Mi cuenta con login | contenido privado |
| Nombre con caracteres especiales | se muestra como texto |
| Cerrar sesion | volver al login |
| Volver a Mi cuenta despues de logout | redireccion a login |
| Ventana incognito | no comparte la sesion normal |

## 11.4 Herramientas del navegador

### Console

Muestra errores de JavaScript y salidas de `console.log`.

### Network

Permite observar:

- metodo GET o POST;
- codigo de estado, como 200 o 302;
- encabezado `Location`;
- recorrido de redirecciones;
- parametros enviados.

### Application o Storage

Permite observar cookies, incluida `PHPSESSID`.

No edites una contrasena real ni la imprimas en la consola.

---

# Parte 12. Codigos HTTP que vas a observar

- `200 OK`: la respuesta se entrego correctamente.
- `302 Found`: PHP envio una redireccion con `header("Location: ...")`.
- `404 Not Found`: la ruta no coincide con un archivo.
- `500 Internal Server Error`: PHP fallo durante la ejecucion.
- `405 Method Not Allowed`: el recurso no acepta ese metodo, si decides implementarlo.

Cuando el navegador sigue automaticamente un 302, a veces solamente ves la pagina final. La pestaña Network permite ver el paso intermedio.

---

# Parte 13. Depuracion ordenada

Cuando algo falle, evita cambiar muchas cosas al mismo tiempo.

## Metodo recomendado

1. Define el comportamiento esperado.
2. Identifica la ultima parte que sabes que funciona.
3. Comprueba una capa por vez.
4. Lee consola y registros.
5. Agrega temporalmente `console.log` en JavaScript.
6. Elimina los logs que ya no aporten.

## Si el mensaje no aparece

1. Existe `#feedback`?
2. La ruta del script es correcta?
3. Hay errores en Console?
4. `getElementById` devuelve un elemento o `null`?
5. La URL contiene `?error=` o `?success=`?
6. El nombre consultado coincide exactamente?

## Si PHP da pagina blanca

1. Revisa `/opt/lampp/logs/error_log`.
2. Ejecuta comprobacion de sintaxis:

```bash
/opt/lampp/bin/php -l php/login.php
```

3. Comprueba Apache y MySQL.
4. Verifica rutas de `require_once`.

## Si el registro falla

1. Los `name` del HTML coinciden con `$_POST`?
2. El formulario usa `method="POST"`?
3. `action` apunta al PHP correcto?
4. La tabla y columnas tienen los nombres esperados?
5. El correo ya existe?

## Si la sesion no funciona

1. Todos los archivos que usan sesion llaman `session_start()`?
2. Se envio contenido antes de `header`?
3. El navegador acepta cookies?
4. La clave usada al guardar coincide con la usada al comprobar?

---

# Parte 14. Proyecto final del material original

Considera terminado el objetivo del primer enlace cuando puedas demostrar:

- [ ] La base y tabla se crean desde SQL.
- [ ] La conexion utiliza `utf8mb4`.
- [ ] El formulario de registro envia POST.
- [ ] PHP valida todos los campos.
- [ ] JavaScript ofrece validacion inmediata.
- [ ] La contrasena se almacena con `password_hash`.
- [ ] El correo no puede repetirse.
- [ ] Las consultas usan placeholders.
- [ ] El registro correcto vuelve con mensaje de exito.
- [ ] Los errores vuelven al formulario.
- [ ] JavaScript lee `error` y `success` de la URL.
- [ ] Login usa `password_verify`.
- [ ] Login regenera el id de sesion.
- [ ] La pagina privada rechaza visitantes sin sesion.
- [ ] Los datos mostrados pasan por `htmlspecialchars`.
- [ ] Logout destruye la sesion.
- [ ] Todas las pruebas negativas tienen resultado controlado.

---

# Parte 15. Version final de referencia

Esta seccion sirve para comparar cuando hayas realizado todas las etapas. No reemplaces tus archivos enteros sin entender las diferencias. Los nombres y rutas deben adaptarse a tu organizacion.

## 15.1 JavaScript de referencia

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const feedback = document.getElementById("feedback");
  const params = new URLSearchParams(window.location.search);

  if (feedback && params.has("error")) {
    feedback.textContent = params.get("error");
    feedback.className = "feedback error";
  } else if (feedback && params.has("success")) {
    feedback.textContent = params.get("success");
    feedback.className = "feedback success";
  }

  const registerForm = document.getElementById("register-form");
  const registerFeedback = document.getElementById("register-feedback");

  if (registerForm && registerFeedback) {
    registerForm.addEventListener("submit", (event) => {
      const name = document.getElementById("register-name").value.trim();
      const password = document.getElementById("register-password").value;

      let message = "";

      if (name === "") {
        message = "El nombre es obligatorio";
      } else if (password.length < 8) {
        message = "La contrasena debe tener al menos 8 caracteres";
      } else if (!/[A-Z]/.test(password)) {
        message = "La contrasena necesita una mayuscula";
      } else if (!/[a-z]/.test(password)) {
        message = "La contrasena necesita una minuscula";
      } else if (!/[0-9]/.test(password)) {
        message = "La contrasena necesita un numero";
      } else if (!/[!@#$%^&*]/.test(password)) {
        message = "La contrasena necesita un caracter especial";
      }

      if (message !== "") {
        event.preventDefault();
        registerFeedback.textContent = message;
        registerFeedback.className = "feedback error";
      }
    });
  }

  document.querySelectorAll(".ojo").forEach((eye) => {
    eye.addEventListener("click", () => {
      const passwordInput = document.getElementById(eye.dataset.target);

      if (!passwordInput) {
        return;
      }

      passwordInput.type =
        passwordInput.type === "password" ? "text" : "password";
    });
  });
});
```

La ultima asignacion usa un operador ternario:

```text
condicion ? valorSiVerdadero : valorSiFalso
```

Es una forma corta de un `if/else`. Si aun te resulta confuso, conserva la version con llaves.

## 15.2 Patron final de error PHP

```php
$mensaje = "Correo o contrasena incorrectos";
header("Location: ../html/login.html?error=" . urlencode($mensaje));
exit();
```

## 15.3 Patron final de exito PHP

```php
$mensaje = "Cuenta creada correctamente";
header("Location: ../html/login.html?success=" . urlencode($mensaje));
exit();
```

## 15.4 Patron de pagina privada

```php
<?php
session_start();

if (!isset($_SESSION["user_id"])) {
    header("Location: login.html?error=" . urlencode("Inicia sesion para continuar"));
    exit();
}
?>
```

## 15.5 Patron de salida HTML segura

```php
<?php
echo htmlspecialchars(
    $_SESSION["user_name"],
    ENT_QUOTES,
    "UTF-8"
);
?>
```

---

# Parte 16. Como explicar el proyecto en una presentacion

## Explicacion corta de treinta segundos

> El proyecto implementa registro e inicio de sesion con PHP y MySQL. Los formularios envian datos por POST. PHP valida los datos, usa consultas preparadas y almacena la contrasena como hash. En el login recupera el usuario y usa `password_verify`. Si es correcto, crea una sesion y protege la pagina Mi cuenta. JavaScript mejora la experiencia mostrando mensajes y validando antes de enviar, pero las validaciones de seguridad permanecen en PHP.

## Preguntas frecuentes

### Por que POST y no GET?

Porque POST envia los datos en el cuerpo de la peticion y esta destinado a operaciones que crean o procesan datos. GET se usa principalmente para obtener recursos y expone parametros en la URL. POST no cifra por si solo; para transporte seguro se necesita HTTPS.

### Por que no guardar la contrasena directamente?

Porque una filtracion revelaria todas las contrasenas. `password_hash` genera una representacion no reversible y `password_verify` permite comprobarla.

### Para que sirve el signo `?` en SQL?

Es un placeholder de una consulta preparada. El valor se vincula por separado para evitar que se interprete como estructura SQL.

### Por que validar en JavaScript y PHP?

JavaScript mejora la experiencia, pero puede desactivarse. PHP protege realmente la aplicacion porque se ejecuta en el servidor.

### Que guarda la sesion?

Guarda temporalmente el id, nombre y correo del usuario autenticado. El navegador mantiene un identificador de sesion en una cookie.

### Para que sirve `exit()` despues de `header()`?

`header` prepara una redireccion, pero PHP podria continuar ejecutando codigo. `exit` detiene la peticion inmediatamente.

### Por que `htmlspecialchars`?

Para que los datos se muestren como texto y no sean interpretados como HTML.

### Por que el mensaje de login es generico?

Para no revelar si una cuenta determinada existe.

---

# Parte 17. Ampliaciones posteriores al material original

Estas funcionalidades no son necesarias para completar el primer enlace, pero son continuaciones naturales.

## 17.1 Editar nombre y correo

Necesitaras:

1. Un formulario con `method="POST"`.
2. Un boton `type="submit"` dentro del formulario.
3. Un script PHP protegido por sesion.
4. Validacion del nuevo nombre y correo.
5. Un `UPDATE usuarios SET name = ?, email = ? WHERE id_user = ?`.
6. Actualizar `$_SESSION` despues del `UPDATE`.

No confundir `method` y `action`:

- `method` define POST o GET;
- `action` define a que URL se envian los datos.

## 17.2 Cambiar contrasena

Debe pedir la contrasena actual, verificarla y luego crear un nuevo hash. Nunca se muestra el hash almacenado.

## 17.3 Recuperar contrasena

Requiere tokens de un solo uso, fecha de expiracion y envio de correo. No se debe enviar la contrasena existente.

## 17.4 Recordarme

La casilla actual es solamente visual. Una implementacion correcta no debe guardar la contrasena en una cookie. Utiliza tokens aleatorios revocables y cookies seguras.

## 17.5 Login con Google o GitHub

Los botones actuales son visuales. Para que funcionen se necesita OAuth, registrar la aplicacion en cada proveedor y validar tokens del lado servidor.

---

# Parte 18. Plan de estudio offline sugerido

## Dia 1

- Repasar arquitectura.
- Completar `textContent`.
- Practicar DOM y `DOMContentLoaded`.
- Leer parametros de URL manuales.

## Dia 2

- Implementar `error` y `success` en JavaScript.
- Crear estilos CSS.
- Probar varias URLs manualmente.

## Dia 3

- Cambiar errores del login de `echo` a redireccion.
- Observar respuestas 302 en Network.
- Explicar `urlencode` y concatenacion.

## Dia 4

- Cambiar registro exitoso a redireccion.
- Implementar deteccion de correo duplicado.
- Probar todos los errores del registro.

## Dia 5

- Agregar ids al formulario de registro.
- Aprender evento `submit` y `preventDefault`.
- Implementar dos reglas de contrasena.

## Dia 6

- Completar reglas de contrasena.
- Implementar mostrar/ocultar contrasena.
- Revisar que PHP siga validando todo.

## Dia 7

- Ejecutar la matriz completa de pruebas.
- Limpiar `console.log` temporales.
- Practicar la explicacion oral.
- Comparar con la lista final.

---

# Parte 19. Glosario

- **Backend:** codigo ejecutado en el servidor, en este caso PHP.
- **Frontend:** HTML, CSS y JavaScript ejecutados o presentados en el navegador.
- **DOM:** representacion en objetos del documento HTML.
- **Evento:** notificacion de que ocurrio una accion.
- **Callback:** funcion que se ejecutara posteriormente.
- **POST:** metodo HTTP usado para enviar datos en el cuerpo.
- **Query string:** parametros colocados despues de `?` en una URL.
- **Redireccion:** respuesta que indica al navegador que abra otra URL.
- **Hash:** transformacion no reversible usada para almacenar contrasenas.
- **Sesion:** almacenamiento temporal asociado a un visitante.
- **Cookie:** pequeno dato guardado por el navegador y enviado al servidor.
- **Consulta preparada:** SQL cuya estructura se separa de sus valores.
- **Placeholder:** posicion reservada, como `?`, para un valor.
- **Validacion:** comprobacion de que un dato cumple reglas.
- **Escapado:** transformacion para mostrar datos sin interpretarlos como codigo.
- **Expresion regular:** patron utilizado para buscar tipos de caracteres.
- **Booleano:** valor `true` o `false`.
- **HTTP 302:** respuesta de redireccion.
- **HTTP 500:** fallo interno durante la ejecucion del servidor.

---

# Cierre

La meta no es memorizar todas las lineas. La meta es poder responder, ante cada linea:

1. Que dato recibe?
2. Que resultado produce?
3. En que lugar se ejecuta: navegador, PHP o MySQL?
4. Que pasa si falla?
5. Como puedo comprobarlo?

Cuando puedas recorrer registro, login, sesion y logout contestando esas cinco preguntas, no solamente tendras una implementacion funcional: vas a entenderla y vas a poder defenderla.
