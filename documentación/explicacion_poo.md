# Aplicación de Programación Orientada a Objetos

## Proyecto

**Gestor Inteligente de Clientes (GIC)**

El Gestor Inteligente de Clientes es una aplicación desarrollada en Python para registrar, consultar, editar y eliminar clientes.

El sistema diferencia entre clientes regulares, premium y corporativos. También incorpora validaciones, excepciones personalizadas, persistencia en SQLite, archivos JSON y CSV, registro de actividades, integraciones externas y una interfaz gráfica desarrollada con Tkinter.

## 1. Programación Orientada a Objetos

La Programación Orientada a Objetos, conocida como POO, es un paradigma que permite organizar un programa mediante clases y objetos.

Una **clase** es una plantilla que define los atributos y métodos que tendrán sus objetos. Un **objeto** es una instancia concreta creada a partir de una clase.

La POO permite desarrollar aplicaciones:

- Modulares.
- Reutilizables.
- Escalables.
- Más fáciles de comprender.
- Más sencillas de mantener.
- Preparadas para incorporar nuevas funcionalidades.

En este proyecto, cada cliente es representado mediante un objeto que contiene sus propios datos y comportamientos.

## 2. Clases y objetos

La clase principal del sistema es `Cliente`. Esta clase representa los datos generales que comparten todos los tipos de clientes.

Sus principales atributos son:

- ID del cliente.
- Nombre.
- Correo electrónico.
- Teléfono.
- Dirección.
- Fecha de registro.

También incluye métodos para consultar y modificar sus datos, calcular descuentos y convertir el objeto en un diccionario.

Ejemplo simplificado de su estructura:

```python
class Cliente:

    def __init__(
        self,
        id_cliente,
        nombre,
        email,
        telefono,
        direccion
    ):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__email = email
        self.__telefono = telefono
        self.__direccion = direccion

    def obtener_id(self):
        return self.__id_cliente

    def obtener_nombre(self):
        return self.__nombre

    def calcular_descuento(self):
        return 0
```

Cuando se crea un cliente concreto, se genera un objeto o instancia de una de las clases del sistema.

Ejemplo:

```python
from modelos.cliente_regular import ClienteRegular

cliente = ClienteRegular(
    id_cliente=1,
    nombre="María Eugenia",
    email="maria@email.cl",
    telefono="+56912345678",
    direccion="Viña del Mar"
)

print(cliente.obtener_nombre())
```

En este ejemplo, `cliente` es un objeto de la clase `ClienteRegular`.

## 3. Encapsulación

La encapsulación consiste en proteger los datos internos de un objeto y controlar la forma en que pueden ser consultados o modificados.

En la clase `Cliente`, los atributos se escriben con doble guion bajo:

```python
self.__id_cliente
self.__nombre
self.__email
self.__telefono
self.__direccion
self.__fecha_registro
```

Esto evita que los atributos sean modificados directamente desde otras partes del programa.

Para obtener sus valores se utilizan métodos accesadores o getters:

```python
def obtener_nombre(self):
    return self.__nombre
```

Para modificar los atributos se utilizan métodos mutadores o setters:

```python
def establecer_nombre(self, nuevo_nombre):
    self.__nombre = Validador.validar_nombre(nuevo_nombre)
```

El setter no modifica el atributo inmediatamente. Primero envía el dato a la clase `Validador`, lo que permite controlar que el nuevo valor cumpla las reglas del sistema.

## 4. Validación de atributos

La clase `Validador` centraliza las reglas utilizadas para revisar los datos ingresados.

Sus métodos son estáticos porque no es necesario crear un objeto de esta clase para utilizarlos.

Ejemplo:

```python
class Validador:

    @staticmethod
    def validar_id(id_cliente):
        id_cliente = int(id_cliente)

        if id_cliente <= 0:
            raise IdInvalidoError(
                "El ID debe ser mayor que cero."
            )

        return id_cliente
```

El sistema valida:

- Que el ID sea un número entero positivo.
- Que el nombre tenga un formato permitido.
- Que el correo electrónico sea válido.
- Que el teléfono contenga entre 9 y 12 dígitos.
- Que la dirección tenga contenido suficiente.
- Que los puntos no sean negativos.
- Que la empresa tenga un nombre válido.
- Que el RUT chileno tenga un dígito verificador correcto.

Esta separación permite reutilizar las validaciones en diferentes partes del programa.

## 5. Herencia

La herencia permite crear nuevas clases a partir de una clase existente.

La clase `Cliente` funciona como clase padre, mientras que las siguientes clases funcionan como clases hijas:

- `ClienteRegular`
- `ClientePremium`
- `ClienteCorporativo`

Su estructura general es:

```python
class ClienteRegular(Cliente):
    pass


class ClientePremium(Cliente):
    pass


class ClienteCorporativo(Cliente):
    pass
```

Las clases hijas reciben los atributos y métodos definidos en `Cliente`, evitando repetir el mismo código en cada tipo de cliente.

## 6. Uso de `super()`

Las clases hijas utilizan `super()` para ejecutar el constructor de la clase padre.

Ejemplo de la clase `ClientePremium`:

```python
class ClientePremium(Cliente):

    def __init__(
        self,
        id_cliente,
        nombre,
        email,
        telefono,
        direccion,
        puntos=0,
        fecha_registro=None
    ):
        super().__init__(
            id_cliente,
            nombre,
            email,
            telefono,
            direccion,
            fecha_registro
        )

        self.__puntos = Validador.validar_puntos(puntos)
```

Mediante `super().__init__()`, la clase `ClientePremium` reutiliza la inicialización de los datos generales y solamente agrega el atributo específico `puntos`.

La clase `ClienteCorporativo` utiliza el mismo principio para agregar:

- Empresa.
- RUT de la empresa.
- Persona de contacto.

## 7. Polimorfismo

El polimorfismo permite que distintas clases respondan al mismo método de maneras diferentes.

En el proyecto, todas las clases de clientes tienen el método:

```python
calcular_descuento()
```

Sin embargo, el resultado depende del tipo de cliente.

```python
class ClienteRegular(Cliente):

    def calcular_descuento(self):
        return 0


class ClientePremium(Cliente):

    def calcular_descuento(self):
        return 10


class ClienteCorporativo(Cliente):

    def calcular_descuento(self):
        return 15
```

Esto permite trabajar con diferentes clientes de una manera uniforme:

```python
clientes = [
    cliente_regular,
    cliente_premium,
    cliente_corporativo
]

for cliente in clientes:
    print(cliente.calcular_descuento())
```

Aunque se utiliza el mismo método, cada objeto entrega un resultado diferente:

- Cliente regular: 0 %.
- Cliente premium: 10 %.
- Cliente corporativo: 15 %.

## 8. Sobrescritura de métodos

La sobrescritura ocurre cuando una clase hija redefine un método heredado de la clase padre.

Además de `calcular_descuento()`, las clases hijas sobrescriben el método `__str__()` para mostrar información específica.

Ejemplo de `ClientePremium`:

```python
def __str__(self):
    return (
        f"{super().__str__()} | "
        f"Tipo: Cliente premium | "
        f"Puntos: {self.__puntos} | "
        f"Descuento: {self.calcular_descuento()}%"
    )
```

El método primero reutiliza el texto generado por la clase padre y luego agrega los puntos y el descuento del cliente premium.

## 9. Métodos especiales

### Método `__str__()`

El método `__str__()` define la representación textual de un objeto.

```python
def __str__(self):
    return (
        f"ID: {self.__id_cliente} | "
        f"Nombre: {self.__nombre} | "
        f"Email: {self.__email} | "
        f"Teléfono: {self.__telefono} | "
        f"Dirección: {self.__direccion}"
    )
```

Gracias a este método, al ejecutar:

```python
print(cliente)
```

se muestra la información del cliente de manera comprensible.

### Método `__eq__()`

El método `__eq__()` permite comparar dos objetos.

```python
def __eq__(self, otro_cliente):

    if not isinstance(otro_cliente, Cliente):
        return False

    return (
        self.__id_cliente
        == otro_cliente.obtener_id()
    )
```

En este proyecto, dos clientes son considerados iguales cuando poseen el mismo ID.

Ejemplo:

```python
cliente_1 = ClienteRegular(
    1,
    "Ana Pérez",
    "ana@email.cl",
    "912345678",
    "Viña del Mar"
)

cliente_2 = ClienteRegular(
    1,
    "Ana Pérez",
    "ana@email.cl",
    "912345678",
    "Viña del Mar"
)

print(cliente_1 == cliente_2)
```

El resultado será:

```text
True
```

## 10. Abstracción

La abstracción permite representar solamente los elementos necesarios para utilizar un objeto, sin obligar al usuario a conocer todos sus detalles internos.

Por ejemplo, para registrar un cliente, la interfaz utiliza el método:

```python
gestor.agregar_cliente(cliente)
```

La interfaz no necesita controlar directamente:

- La conexión con SQLite.
- La escritura del archivo JSON.
- La exportación del archivo CSV.
- La generación del registro de actividad.
- La validación externa del correo.
- El envío de la bienvenida.

Estas tareas son coordinadas internamente por `GestorClientes`.

## 11. Colaboración entre objetos

El proyecto utiliza varias clases que colaboran para completar las operaciones.

La clase `GestorClientes` trabaja con objetos de:

- `BaseDatos`
- `GestorArchivos`
- `RegistroActividad`
- `ValidadorEmailAPI`
- `ServicioEmailBienvenida`

Su constructor permite recibir estos objetos o crearlos automáticamente:

```python
class GestorClientes:

    def __init__(
        self,
        base_datos=None,
        gestor_archivos=None,
        registro_actividad=None,
        validador_email_api=None,
        servicio_email=None
    ):
        self.__base_datos = (
            base_datos
            if base_datos is not None
            else BaseDatos()
        )

        self.__gestor_archivos = (
            gestor_archivos
            if gestor_archivos is not None
            else GestorArchivos()
        )

        self.__registro_actividad = (
            registro_actividad
            if registro_actividad is not None
            else RegistroActividad()
        )
```

Esta estructura permite dividir las responsabilidades del sistema:

- `GestorClientes` coordina las operaciones.
- `BaseDatos` administra SQLite.
- `GestorArchivos` administra JSON y CSV.
- `RegistroActividad` guarda los logs.
- `ValidadorEmailAPI` gestiona la validación externa.
- `ServicioEmailBienvenida` gestiona las notificaciones.

## 12. Composición y agregación

En el sistema existen relaciones en las que una clase contiene o utiliza objetos de otras clases.

La interfaz gráfica contiene un objeto `GestorClientes`, que es utilizado para ejecutar todas las operaciones solicitadas por el usuario.

Por su parte, `GestorClientes` utiliza objetos de las clases encargadas de la persistencia, archivos, registros e integraciones.

Estas relaciones permiten que cada clase tenga una responsabilidad específica y que el sistema sea más sencillo de mantener o ampliar.

## 13. Manejo de excepciones

El proyecto utiliza excepciones personalizadas para controlar errores específicos.

Entre ellas se encuentran:

- `IdInvalidoError`
- `NombreInvalidoError`
- `EmailInvalidoError`
- `TelefonoInvalidoError`
- `DireccionInvalidaError`
- `RutInvalidoError`
- `PuntosInvalidosError`
- `ClienteDuplicadoError`
- `ClienteNoEncontradoError`
- `ErrorBaseDatos`
- `ErrorJSON`
- `ErrorCSV`
- `ErrorAPIExterna`
- `ErrorNotificacion`

Ejemplo:

```python
if self.existe_cliente(cliente.obtener_id()):
    raise ClienteDuplicadoError(
        f"Ya existe un cliente con el ID "
        f"{cliente.obtener_id()}."
    )
```

El uso de excepciones permite mostrar mensajes claros y evita que el programa se cierre inesperadamente ante un dato inválido.

## 14. Persistencia de datos

El sistema conserva la información mediante diferentes mecanismos:

### SQLite

SQLite funciona como almacenamiento principal de los clientes. Permite crear, consultar, actualizar y eliminar registros.

### JSON

El archivo JSON permite mantener una representación estructurada de los clientes.

### CSV

El archivo CSV facilita la revisión y el intercambio de información mediante programas de hojas de cálculo.

### Registro de actividades

El archivo de actividades conserva una trazabilidad de las operaciones realizadas en el sistema.

La persistencia permite que los datos continúen disponibles después de cerrar y volver a abrir la aplicación.

## 15. Ejemplo completo de uso

```python
from modelos.cliente_regular import ClienteRegular
from modelos.cliente_premium import ClientePremium
from modelos.cliente_corporativo import ClienteCorporativo

cliente_regular = ClienteRegular(
    id_cliente=1,
    nombre="Ana Pérez",
    email="ana@email.cl",
    telefono="+56912345678",
    direccion="Viña del Mar"
)

cliente_premium = ClientePremium(
    id_cliente=2,
    nombre="María González",
    email="maria@email.cl",
    telefono="+56987654321",
    direccion="Valparaíso",
    puntos=100
)

cliente_corporativo = ClienteCorporativo(
    id_cliente=3,
    nombre="Pedro Soto",
    email="pedro@empresa.cl",
    telefono="+56911223344",
    direccion="Quilpué",
    empresa="SolutionTech",
    rut_empresa="76123456-0",
    contacto="Pedro Soto"
)

clientes = [
    cliente_regular,
    cliente_premium,
    cliente_corporativo
]

for cliente in clientes:
    print(cliente)
    print(
        "Descuento:",
        cliente.calcular_descuento(),
        "%"
    )
```

Este ejemplo demuestra:

- Creación de objetos.
- Herencia.
- Uso de constructores.
- Uso de `super()`.
- Encapsulación.
- Polimorfismo.
- Sobrescritura de métodos.
- Diferenciación de tipos de clientes.

## Conclusión

El Gestor Inteligente de Clientes aplica los principales conceptos de la Programación Orientada a Objetos.

La clase `Cliente` reúne los atributos y comportamientos comunes, mientras que `ClienteRegular`, `ClientePremium` y `ClienteCorporativo` especializan su funcionamiento mediante herencia y polimorfismo.

La encapsulación protege los datos, las validaciones controlan la información ingresada y las excepciones personalizadas permiten responder adecuadamente ante errores.

Además, la colaboración entre objetos permite separar las responsabilidades de la interfaz, la lógica de negocio, la persistencia, los archivos, los registros y las integraciones externas.

Gracias a esta estructura, el proyecto es modular, reutilizable, mantenible y preparado para incorporar futuras mejoras.