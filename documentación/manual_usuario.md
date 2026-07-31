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

La información se almacena en una base de datos SQLite y también puede exportarse a archivos JSON y CSV.

Además, el sistema mantiene un registro de las actividades realizadas por el usuario.

---

## 2. Requisitos para ejecutar la aplicación

Para utilizar el sistema se necesita:

- Tener Python 3 instalado.
- Tener acceso a una terminal o PowerShell.
- Tener todos los archivos del proyecto dentro de la misma carpeta.
- Ejecutar el programa desde la carpeta principal del proyecto.

La aplicación utiliza principalmente módulos incluidos en Python, por lo que no requiere instalar bibliotecas externas para su funcionamiento básico.

---

## 3. Estructura principal del proyecto

El proyecto está organizado en las siguientes carpetas:

### modelos

Contiene las clases relacionadas con los clientes:

- `cliente.py`
- `cliente_regular.py`
- `cliente_premium.py`
- `cliente_corporativo.py`

### servicios

Contiene las funcionalidades internas del sistema:

- Validaciones.
- Manejo de excepciones.
- Gestión de clientes.
- Conexión con SQLite.
- Exportación de archivos.
- Registro de actividades.
- Integraciones externas.

### interfaz

Contiene la ventana principal desarrollada con Tkinter.

### datos

Contiene los archivos generados por el sistema:

- Base de datos SQLite.
- Archivo JSON.
- Archivo CSV.
- Registro de actividades.

### pruebas

Contiene las pruebas unitarias del proyecto.

### documentación

Contiene el diagrama UML, las explicaciones técnicas, las capturas y este manual de usuario.

---

## 4. Cómo iniciar la aplicación

Para iniciar el programa:

1. Abrir Visual Studio Code.
2. Abrir la carpeta `gestor-inteligente-clientes`.
3. Abrir una terminal.
4. Verificar que la terminal se encuentre en la carpeta principal del proyecto.
5. Ejecutar el siguiente comando:

```powershell
python main.py