# Manual de Usuario

## Gestor Inteligente de Clientes

**Proyecto:** Gestor Inteligente de Clientes (GIC)  
**Empresa solicitante:** SolutionTech  
**Lenguaje:** Python 3  
**Interfaz:** Tkinter  
**Autora:** María Eugenia Perinetti Aspee  

---

## 1. Descripción del sistema

El Gestor Inteligente de Clientes es una aplicación desarrollada en Python que permite registrar, consultar, modificar y eliminar información de clientes.

El sistema utiliza Programación Orientada a Objetos y permite trabajar con tres tipos de clientes:

- Cliente Regular.
- Cliente Premium.
- Cliente Corporativo.

La información se almacena principalmente en una base de datos SQLite. También puede exportarse a archivos JSON y CSV.

Además, la aplicación mantiene un registro de las actividades realizadas y dispone de servicios para validar correos electrónicos y enviar mensajes de bienvenida.

---

## 2. Requisitos para ejecutar la aplicación

Para utilizar el sistema se necesita:

- Tener Python 3 instalado.
- Tener disponible Tkinter.
- Tener acceso a una terminal o PowerShell.
- Mantener todos los archivos del proyecto dentro de su estructura original.
- Ejecutar el programa desde la carpeta principal del proyecto.

La aplicación utiliza principalmente módulos incluidos en Python, por lo que no requiere instalar bibliotecas externas para su funcionamiento básico.

Para comprobar la versión de Python instalada se puede ejecutar:

```powershell
python --version
```

También puede utilizarse:

```powershell
py --version
```

---

## 3. Estructura principal del proyecto

El proyecto está organizado en las siguientes carpetas:

### `modelos`

Contiene las clases relacionadas con los clientes:

- `cliente.py`
- `cliente_regular.py`
- `cliente_premium.py`
- `cliente_corporativo.py`

### `servicios`

Contiene las funcionalidades internas del sistema:

- Gestión de clientes.
- Validación de datos.
- Manejo de excepciones.
- Conexión con SQLite.
- Lectura y escritura de JSON y CSV.
- Registro de actividades.
- Integraciones externas.

### `interfaz`

Contiene la ventana principal desarrollada con Tkinter.

### `datos`

Contiene los archivos generados por el sistema:

- Base de datos SQLite.
- Archivo JSON.
- Archivo CSV.
- Registro de actividades.

### `pruebas`

Contiene las pruebas unitarias del proyecto.

### `documentación`

Contiene:

- Diagrama de clases UML.
- Código PlantUML.
- Explicación de Programación Orientada a Objetos.
- Manual de usuario.

Las capturas de funcionamiento se adjuntan por separado junto con la entrega.

---

## 4. Cómo iniciar la aplicación

Para iniciar el programa:

1. Abrir Visual Studio Code.
2. Seleccionar **File → Open Folder**.
3. Abrir la carpeta `gestor-inteligente-clientes`.
4. Abrir una terminal desde el menú **Terminal → New Terminal**.
5. Verificar que la terminal se encuentre en la carpeta principal del proyecto.
6. Ejecutar:

```powershell
python main.py
```

Si el comando anterior no funciona, utilizar:

```powershell
py main.py
```

Al ejecutar el programa se abrirá la ventana principal del Gestor Inteligente de Clientes.

---

## 5. Elementos de la interfaz

La interfaz contiene formularios, botones y una tabla para administrar los clientes.

Entre sus principales funciones se encuentran:

- Registrar clientes.
- Buscar clientes.
- Modificar información.
- Eliminar registros.
- Agregar puntos a clientes premium.
- Exportar información.
- Consultar el registro de actividades.
- Limpiar el formulario.

La tabla principal muestra los clientes almacenados en el sistema.

---

## 6. Registrar un cliente regular

Para registrar un cliente regular:

1. Seleccionar el tipo **Regular**.
2. Ingresar el ID.
3. Ingresar el nombre.
4. Ingresar el correo electrónico.
5. Ingresar el teléfono.
6. Ingresar la dirección.
7. Presionar el botón de registro.

El cliente regular no requiere puntos, empresa ni RUT empresarial.

Este tipo de cliente tiene un descuento de:

```text
0 %
```

---

## 7. Registrar un cliente premium

Para registrar un cliente premium:

1. Seleccionar el tipo **Premium**.
2. Completar los datos generales.
3. Ingresar la cantidad inicial de puntos.
4. Presionar el botón de registro.

Los puntos deben ser un número entero igual o superior a cero.

Este tipo de cliente tiene un descuento de:

```text
10 %
```

Los clientes premium permiten utilizar la opción de agregar puntos después de haber sido registrados.

---

## 8. Registrar un cliente corporativo

Para registrar un cliente corporativo:

1. Seleccionar el tipo **Corporativo**.
2. Completar los datos generales.
3. Ingresar el nombre de la empresa.
4. Ingresar el RUT de la empresa.
5. Ingresar el nombre de la persona de contacto.
6. Presionar el botón de registro.

El RUT debe incluir un dígito verificador válido.

Este tipo de cliente tiene un descuento de:

```text
15 %
```

---

## 9. Validaciones de datos

La aplicación revisa los datos antes de guardar un cliente.

### ID

- Debe ser un número entero.
- Debe ser mayor que cero.
- No puede repetirse.

### Nombre

- No puede estar vacío.
- Debe cumplir el formato definido por el sistema.

### Correo electrónico

- Debe contener una estructura válida.
- Debe incluir un nombre de usuario, el símbolo `@` y un dominio.

Ejemplo válido:

```text
cliente@email.cl
```

### Teléfono

- Debe contener una cantidad válida de dígitos.
- Puede incluir el código de Chile.

Ejemplo:

```text
+56912345678
```

### Dirección

- No puede quedar vacía.
- Debe contener información suficiente.

### Puntos

- Deben ser números enteros.
- No pueden ser negativos.
- Solo corresponden a clientes premium.

### RUT empresarial

- Debe respetar el formato de un RUT chileno.
- Debe tener un dígito verificador correcto.

Cuando un dato es inválido, la aplicación muestra un mensaje explicando el problema.

---

## 10. Buscar un cliente

Para buscar un cliente:

1. Ingresar el ID del cliente.
2. Presionar el botón **Buscar**.
3. El sistema mostrará la información encontrada.

Si el ID no existe, se mostrará un mensaje indicando que el cliente no fue encontrado.

---

## 11. Modificar un cliente

Para modificar la información de un cliente:

1. Buscar o seleccionar el cliente en la tabla.
2. Revisar los datos cargados en el formulario.
3. Modificar los campos necesarios.
4. Presionar el botón **Actualizar**.
5. Confirmar la operación si la aplicación lo solicita.

El sistema volverá a validar los datos antes de guardar los cambios.

El ID funciona como identificador único y no debe asignarse a otro cliente.

---

## 12. Eliminar un cliente

Para eliminar un cliente:

1. Seleccionar el cliente en la tabla.
2. Presionar el botón **Eliminar**.
3. Confirmar la eliminación.

Después de confirmar, el cliente será eliminado de la base de datos y la tabla se actualizará.

Esta operación también quedará registrada en el archivo de actividades.

---

## 13. Agregar puntos a un cliente premium

Para agregar puntos:

1. Seleccionar un cliente premium.
2. Ingresar la cantidad de puntos.
3. Presionar la opción correspondiente para agregar puntos.
4. Confirmar la operación.

Los puntos:

- Deben ser enteros.
- Deben ser mayores que cero.
- Solo pueden agregarse a clientes premium.

Si se intenta agregar puntos a un cliente regular o corporativo, la aplicación mostrará un mensaje de error.

---

## 14. Limpiar el formulario

La opción de limpieza permite borrar los datos mostrados en los campos de la interfaz.

Esta función:

- No elimina clientes.
- No modifica la base de datos.
- Solo deja vacío el formulario para realizar una nueva operación.

---

## 15. Exportar información

La aplicación permite exportar la información almacenada.

Al utilizar la opción de exportación se actualizan los archivos:

```text
datos/clientes.json
datos/clientes.csv
```

### Archivo JSON

Guarda la información de los clientes en una estructura organizada mediante claves y valores.

### Archivo CSV

Guarda la información en un formato compatible con programas de hojas de cálculo.

La exportación no elimina los datos de SQLite.

---

## 16. Base de datos SQLite

La aplicación utiliza SQLite como sistema principal de persistencia.

La base de datos permite:

- Insertar clientes.
- Buscar clientes.
- Listar clientes.
- Actualizar registros.
- Eliminar clientes.
- Conservar la información después de cerrar el programa.

Al volver a iniciar la aplicación, los clientes registrados deben continuar disponibles.

---

## 17. Registro de actividades

Las operaciones realizadas quedan almacenadas en un archivo de registro.

Entre las acciones registradas pueden encontrarse:

- Creación de clientes.
- Actualización de información.
- Eliminación de clientes.
- Exportación de archivos.
- Validación de correos.
- Envío o simulación de mensajes de bienvenida.
- Errores controlados.

El registro permite mantener trazabilidad sobre el uso del sistema.

---

## 18. Integraciones externas

La aplicación contempla dos servicios:

- Validación externa de correos electrónicos.
- Envío de mensajes de bienvenida.

Las claves privadas no se incluyen en el repositorio.

### Modo demostración

Cuando no existen claves configuradas, el sistema funciona en modo demostración.

En este modo:

- Se mantienen las validaciones locales.
- Se simula la validación externa.
- Se simula el envío del mensaje de bienvenida.
- Se registra la operación.
- La aplicación continúa funcionando normalmente.

### Activación mediante variables de entorno

Las integraciones pueden activarse mediante variables de entorno configuradas en PowerShell.

Ejemplo:

```powershell
$env:GIC_ACTIVAR_APIS="1"
$env:ABSTRACT_EMAIL_API_KEY="CLAVE_PRIVADA"
$env:BREVO_API_KEY="CLAVE_PRIVADA"
$env:BREVO_REMITENTE_EMAIL="correo@ejemplo.cl"
$env:BREVO_REMITENTE_NOMBRE="SolutionTech"

python main.py
```

Las claves reales nunca deben subirse a GitHub.

---

## 19. Ejecución de las pruebas unitarias

Para ejecutar las pruebas:

1. Cerrar la aplicación si se encuentra abierta.
2. Abrir la terminal en la carpeta principal.
3. Ejecutar:

```powershell
python -m unittest discover -s pruebas -p "test_*.py" -v
```

El resultado esperado debe finalizar con:

```text
OK
```

Las pruebas verifican, entre otros elementos:

- Creación de clientes.
- Herencia y polimorfismo.
- Métodos especiales.
- Validaciones.
- Manejo de clientes duplicados.
- Persistencia en SQLite.
- Archivos JSON y CSV.
- Registro de actividades.
- Operaciones del gestor.

---

## 20. Solución de problemas

### Python no se reconoce

Probar con:

```powershell
py main.py
```

También se debe comprobar que Python esté agregado a las variables de entorno de Windows.

### La ventana no se abre

Revisar que:

- `main.py` se ejecute desde la carpeta principal.
- La estructura de carpetas no haya sido modificada.
- Tkinter esté disponible.

Para comprobar Tkinter:

```powershell
python -m tkinter
```

### El ID ya existe

Cada cliente debe tener un ID único.

Se debe utilizar un número que no esté asignado a otro cliente.

### El correo electrónico es rechazado

Revisar que tenga una estructura como:

```text
nombre@dominio.cl
```

### El teléfono es rechazado

Ingresar solo los caracteres permitidos y una cantidad válida de dígitos.

### El RUT es inválido

Revisar:

- El número.
- El dígito verificador.
- El formato ingresado.

### No se envía el correo de bienvenida

La aplicación puede estar funcionando en modo demostración.

Para realizar un envío real deben configurarse las variables de entorno y las claves correspondientes.

### La base de datos está bloqueada

Cerrar otras ventanas o procesos que puedan estar utilizando la aplicación y volver a intentarlo.

### Los datos no aparecen después de reiniciar

Comprobar que:

- La carpeta `datos` exista.
- El programa tenga permisos de escritura.
- El archivo SQLite no haya sido eliminado.
- La aplicación se esté ejecutando desde la carpeta correcta.

### Aparece un error durante la exportación

Revisar que:

- La carpeta `datos` exista.
- Los archivos no estén abiertos en otro programa.
- El sistema tenga permisos de escritura.

---

## 21. Cierre correcto de la aplicación

Para cerrar el programa:

1. Finalizar cualquier operación pendiente.
2. Cerrar la ventana principal mediante la `X`.
3. Confirmar el cierre si el sistema lo solicita.

La información registrada permanece almacenada en SQLite.

---

## 22. Recomendaciones de seguridad

- No compartir claves privadas.
- No subir archivos `.env` a GitHub.
- No modificar directamente la base de datos.
- Mantener copias de respaldo.
- Verificar los datos antes de eliminar un cliente.
- Ejecutar las pruebas después de realizar cambios importantes.

---

## 23. Conclusión

El Gestor Inteligente de Clientes ofrece una solución para administrar distintos tipos de clientes mediante una interfaz gráfica.

La aplicación permite registrar, buscar, editar y eliminar información, aplicar validaciones, conservar los datos en SQLite, exportar archivos JSON y CSV, registrar actividades y utilizar integraciones externas.

Su estructura modular facilita el mantenimiento y permite incorporar futuras funcionalidades sin alterar completamente el sistema.