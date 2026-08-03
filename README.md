# Gestor Inteligente de Clientes

Proyecto desarrollado en Python para la empresa ficticia **SolutionTech**.

El sistema permite registrar, consultar, actualizar y eliminar clientes mediante una interfaz gráfica, aplicando Programación Orientada a Objetos, validaciones, manejo de excepciones, persistencia de datos y pruebas unitarias.

## Autora

**María Eugenia Perinetti Aspee**

---

## Descripción

El Gestor Inteligente de Clientes permite administrar información de distintos tipos de clientes:

- Clientes regulares.
- Clientes premium.
- Clientes corporativos.

La aplicación cuenta con una interfaz gráfica desarrollada con Tkinter y almacena la información en una base de datos SQLite.

También genera respaldos en formatos JSON y CSV y mantiene un registro de las actividades realizadas.

---

## Funcionalidades principales

- Registrar clientes.
- Buscar clientes por ID.
- Modificar información de clientes.
- Eliminar clientes.
- Listar clientes en una tabla.
- Gestionar clientes regulares.
- Gestionar clientes premium.
- Gestionar clientes corporativos.
- Asignar puntos a clientes premium.
- Calcular descuentos según el tipo de cliente.
- Validar los datos ingresados.
- Evitar clientes con ID repetido.
- Guardar información en SQLite.
- Exportar información a JSON.
- Exportar información a CSV.
- Registrar actividades en un archivo log.
- Simular la validación externa de correos.
- Simular el envío de mensajes de bienvenida.
- Ejecutar pruebas unitarias.

---

## Tipos de clientes

### Cliente Regular

- No posee puntos.
- No tiene descuento especial.
- Utiliza los datos generales de la clase `Cliente`.

### Cliente Premium

- Puede acumular puntos.
- Posee un descuento del 10 %.
- Permite modificar y agregar puntos.

### Cliente Corporativo

- Registra el nombre de la empresa.
- Registra el RUT de la empresa.
- Registra una persona de contacto.
- Posee un descuento del 15 %.

---

## Tecnologías utilizadas

- Python 3.
- Tkinter.
- SQLite.
- JSON.
- CSV.
- Programación Orientada a Objetos.
- Unittest.
- PlantUML.
- Visual Studio Code.
- Git y GitHub.

---

## Conceptos de Programación Orientada a Objetos

El proyecto utiliza los siguientes conceptos:

### Clases y objetos

Cada cliente es representado mediante un objeto creado a partir de una clase.

### Encapsulación

Los atributos de los clientes se encuentran protegidos mediante atributos privados y métodos de acceso.

### Herencia

Las clases `ClienteRegular`, `ClientePremium` y `ClienteCorporativo` heredan de la clase principal `Cliente`.

### Polimorfismo

Cada tipo de cliente implementa su propio método `calcular_descuento()`.

### Composición

La clase `GestorClientes` utiliza objetos de las clases:

- `BaseDatos`
- `GestorArchivos`
- `RegistroActividad`
- `ValidadorEmailAPI`
- `ServicioEmailBienvenida`

---

## Estructura del proyecto

```text
gestor-inteligente-clientes/
│
├── main.py
├── README.md
├── .gitignore
│
├── modelos/
│   ├── __init__.py
│   ├── cliente.py
│   ├── cliente_regular.py
│   ├── cliente_premium.py
│   └── cliente_corporativo.py
│
├── servicios/
│   ├── __init__.py
│   ├── base_datos.py
│   ├── excepciones.py
│   ├── gestor_archivos.py
│   ├── gestor_clientes.py
│   ├── integraciones.py
│   ├── registro_actividad.py
│   └── validaciones.py
│
├── interfaz/
│   ├── __init__.py
│   └── ventana_principal.py
│
├── datos/
│   ├── clientes.db
│   ├── clientes.json
│   ├── clientes.csv
│   └── actividades.log
│
├── pruebas/
│   ├── __init__.py
│   └── test_clientes.py
│
└── documentación/
    ├── diagrama_clases.png
    ├── diagrama_clases.puml
    ├── explicacion_poo.md
    └── manual_usuario.md
```

---

## Cómo ejecutar la aplicación

### 1. Abrir el proyecto

Abrir la carpeta `gestor-inteligente-clientes` en Visual Studio Code.

### 2. Abrir una terminal

La terminal debe encontrarse en la carpeta principal del proyecto.

### 3. Ejecutar el programa

```powershell
python main.py
```

Después de ejecutar el comando se abrirá la interfaz gráfica del sistema.

---

## Uso de la aplicación

### Registrar un cliente

1. Ingresar un ID único.
2. Escribir el nombre.
3. Ingresar el correo electrónico.
4. Ingresar el teléfono.
5. Escribir la dirección.
6. Seleccionar el tipo de cliente.
7. Completar los campos especiales cuando corresponda.
8. Presionar `Registrar`.

### Buscar un cliente

1. Ingresar el ID.
2. Presionar `Buscar`.

### Actualizar un cliente

1. Seleccionar el cliente en la tabla.
2. Modificar sus datos.
3. Presionar `Actualizar`.

### Eliminar un cliente

1. Seleccionar el cliente.
2. Presionar `Eliminar`.
3. Confirmar la eliminación.

### Exportar información

Presionar el botón `Exportar` para actualizar los archivos JSON y CSV.

---

## Persistencia de datos

La aplicación utiliza SQLite como sistema principal de almacenamiento.

La base de datos se encuentra en:

```text
datos/clientes.db
```

También se generan los siguientes archivos:

```text
datos/clientes.json
datos/clientes.csv
datos/actividades.log
```

---

## Validaciones

El sistema valida:

- ID numérico y positivo.
- ID no repetido.
- Nombre válido.
- Correo electrónico válido.
- Teléfono válido.
- Dirección obligatoria.
- Puntos numéricos y no negativos.
- RUT de empresa válido.
- Campos obligatorios para clientes corporativos.
- Tipo de cliente permitido.

---

## Manejo de excepciones

El proyecto incluye excepciones personalizadas para controlar:

- Datos inválidos.
- Clientes duplicados.
- Clientes inexistentes.
- Errores de archivos.
- Errores de SQLite.
- Errores de integraciones externas.
- Errores de notificaciones.

Esto permite mostrar mensajes comprensibles y evitar que el programa se cierre inesperadamente.

---

## Integraciones externas

El sistema contiene una estructura para:

- Validar correos mediante una API externa.
- Enviar mensajes de bienvenida.

Para la entrega académica estas funciones trabajan en modo demostración.

En este modo:

- No se utilizan claves privadas.
- No se realizan conexiones externas.
- La validación del correo se simula.
- El mensaje de bienvenida se simula.
- Las operaciones quedan registradas en `actividades.log`.

---

## Pruebas unitarias

Para ejecutar las pruebas se debe cerrar previamente la interfaz gráfica.

Luego, en la terminal, ejecutar:

```powershell
python -m unittest discover -s pruebas -p "test_*.py" -v
```

El resultado correcto debe finalizar con:

```text
OK
```

---

## Diagrama de clases

El diagrama UML del sistema se encuentra en:

```text
documentación/diagrama_clases.png
```

El archivo original de PlantUML se encuentra en:

```text
documentación/diagrama_clases.puml
```

---

## Documentación

El proyecto incluye:

 diagrama_clases.png
 diagrama_clases.puml
 explicacion_poo.md
 manual_usuario.md

---

## Estado del proyecto

El sistema permite realizar las operaciones principales de gestión de clientes y cuenta con persistencia, validaciones, manejo de errores, interfaz gráfica, documentación y pruebas unitarias.