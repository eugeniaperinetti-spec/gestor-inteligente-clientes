import sqlite3

from contextlib import contextmanager
from pathlib import Path

from modelos.cliente import Cliente
from modelos.cliente_regular import ClienteRegular
from modelos.cliente_premium import ClientePremium
from modelos.cliente_corporativo import ClienteCorporativo

from servicios.validaciones import Validador

from servicios.excepciones import (
    ErrorBaseDatos,
    ClienteNoEncontradoError,
    TipoClienteInvalidoError,
    ErrorValidacion
)


class BaseDatos:
    """
    Gestiona la persistencia de clientes en SQLite.
    """

    def __init__(self, ruta_base_datos=None):
        carpeta_proyecto = Path(__file__).resolve().parent.parent
        carpeta_datos = carpeta_proyecto / "datos"

        carpeta_datos.mkdir(
            parents=True,
            exist_ok=True
        )

        if ruta_base_datos is None:
            self.__ruta_base_datos = (
                carpeta_datos / "clientes.db"
            )
        else:
            self.__ruta_base_datos = Path(
                ruta_base_datos
            )

        self.crear_tabla()

    @contextmanager
    def __conexion(self):
        """
        Abre una conexión, confirma los cambios y la cierra.
        """

        conexion = None

        try:
            conexion = sqlite3.connect(
                str(self.__ruta_base_datos)
            )

            conexion.row_factory = sqlite3.Row

            yield conexion

            conexion.commit()

        except sqlite3.Error:
            if conexion is not None:
                conexion.rollback()

            raise

        finally:
            if conexion is not None:
                conexion.close()

    def crear_tabla(self):
        """
        Crea la tabla clientes si todavía no existe.
        """

        consulta = """
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                fecha_registro TEXT NOT NULL,
                tipo_cliente TEXT NOT NULL,
                puntos INTEGER DEFAULT 0,
                empresa TEXT,
                rut_empresa TEXT,
                contacto TEXT
            )
        """

        try:
            with self.__conexion() as conexion:
                conexion.execute(consulta)

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudo crear la tabla clientes: {error}"
            )

    @staticmethod
    def __validar_cliente(cliente):
        if not isinstance(cliente, Cliente):
            raise TipoClienteInvalidoError(
                "Solo se pueden guardar objetos de tipo Cliente."
            )

    @staticmethod
    def __obtener_datos_cliente(cliente):
        """
        Convierte un cliente en una tupla para SQLite.
        """

        BaseDatos.__validar_cliente(cliente)

        datos = cliente.convertir_a_diccionario()

        return (
            datos["id_cliente"],
            datos["nombre"],
            datos["email"],
            datos["telefono"],
            datos["direccion"],
            datos["fecha_registro"],
            datos["tipo_cliente"],
            datos.get("puntos", 0),
            datos.get("empresa"),
            datos.get("rut_empresa"),
            datos.get("contacto")
        )

    @staticmethod
    def __crear_cliente_desde_fila(fila):
        """
        Reconstruye el tipo correcto de cliente.
        """

        tipo_cliente = fila["tipo_cliente"]

        id_cliente = fila["id_cliente"]
        nombre = fila["nombre"]
        email = fila["email"]
        telefono = fila["telefono"]
        direccion = fila["direccion"]
        fecha_registro = fila["fecha_registro"]

        if tipo_cliente == "ClienteRegular":
            return ClienteRegular(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                fecha_registro
            )

        if tipo_cliente == "ClientePremium":
            return ClientePremium(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                fila["puntos"] or 0,
                fecha_registro
            )

        if tipo_cliente == "ClienteCorporativo":
            return ClienteCorporativo(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                fila["empresa"],
                fila["rut_empresa"],
                fila["contacto"],
                fecha_registro
            )

        if tipo_cliente == "Cliente":
            return Cliente(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                fecha_registro
            )

        raise ErrorBaseDatos(
            f"El tipo de cliente '{tipo_cliente}' "
            f"no está reconocido."
        )

    def guardar_cliente(self, cliente):
        """
        Guarda un cliente nuevo.
        """

        datos = self.__obtener_datos_cliente(cliente)

        consulta = """
            INSERT INTO clientes (
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                fecha_registro,
                tipo_cliente,
                puntos,
                empresa,
                rut_empresa,
                contacto
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            with self.__conexion() as conexion:
                conexion.execute(
                    consulta,
                    datos
                )

        except sqlite3.IntegrityError:
            raise ErrorBaseDatos(
                f"Ya existe un cliente con el ID "
                f"{cliente.obtener_id()} en SQLite."
            )

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudo guardar el cliente: {error}"
            )

        return True

    def guardar_clientes(self, clientes):
        """
        Guarda varios clientes.
        """

        try:
            lista_clientes = list(clientes)

        except TypeError:
            raise ErrorBaseDatos(
                "Los clientes deben estar contenidos en una lista."
            )

        consulta = """
            INSERT INTO clientes (
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                fecha_registro,
                tipo_cliente,
                puntos,
                empresa,
                rut_empresa,
                contacto
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            with self.__conexion() as conexion:
                for cliente in lista_clientes:
                    conexion.execute(
                        consulta,
                        self.__obtener_datos_cliente(cliente)
                    )

        except sqlite3.IntegrityError as error:
            raise ErrorBaseDatos(
                f"No se pudieron guardar los clientes. "
                f"Puede existir un ID duplicado: {error}"
            )

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudieron guardar los clientes: {error}"
            )

        return len(lista_clientes)

    def obtener_clientes(self):
        """
        Recupera todos los clientes almacenados.
        """

        consulta = """
            SELECT
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                fecha_registro,
                tipo_cliente,
                puntos,
                empresa,
                rut_empresa,
                contacto
            FROM clientes
            ORDER BY id_cliente
        """

        try:
            with self.__conexion() as conexion:
                filas = conexion.execute(
                    consulta
                ).fetchall()

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudieron consultar los clientes: "
                f"{error}"
            )

        clientes = []

        for numero_fila, fila in enumerate(
            filas,
            start=1
        ):
            try:
                cliente = self.__crear_cliente_desde_fila(
                    fila
                )

                clientes.append(cliente)

            except (
                ErrorValidacion,
                KeyError,
                TypeError,
                ValueError
            ) as error:
                raise ErrorBaseDatos(
                    f"Los datos de la fila {numero_fila} "
                    f"no son válidos: {error}"
                )

        return clientes

    def buscar_cliente(self, id_cliente):
        """
        Busca un cliente por su ID.
        """

        id_cliente = Validador.validar_id(id_cliente)

        consulta = """
            SELECT
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                fecha_registro,
                tipo_cliente,
                puntos,
                empresa,
                rut_empresa,
                contacto
            FROM clientes
            WHERE id_cliente = ?
        """

        try:
            with self.__conexion() as conexion:
                fila = conexion.execute(
                    consulta,
                    (id_cliente,)
                ).fetchone()

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudo buscar el cliente: {error}"
            )

        if fila is None:
            raise ClienteNoEncontradoError(
                f"No existe un cliente con el ID "
                f"{id_cliente} en SQLite."
            )

        try:
            return self.__crear_cliente_desde_fila(fila)

        except (
            ErrorValidacion,
            KeyError,
            TypeError,
            ValueError
        ) as error:
            raise ErrorBaseDatos(
                f"Los datos almacenados no son válidos: {error}"
            )

    def actualizar_cliente(self, cliente):
        """
        Actualiza un cliente existente.
        """

        datos = self.__obtener_datos_cliente(cliente)

        consulta = """
            UPDATE clientes
            SET
                nombre = ?,
                email = ?,
                telefono = ?,
                direccion = ?,
                fecha_registro = ?,
                tipo_cliente = ?,
                puntos = ?,
                empresa = ?,
                rut_empresa = ?,
                contacto = ?
            WHERE id_cliente = ?
        """

        datos_actualizacion = (
            datos[1],
            datos[2],
            datos[3],
            datos[4],
            datos[5],
            datos[6],
            datos[7],
            datos[8],
            datos[9],
            datos[10],
            datos[0]
        )

        try:
            with self.__conexion() as conexion:
                cursor = conexion.execute(
                    consulta,
                    datos_actualizacion
                )

                if cursor.rowcount == 0:
                    raise ClienteNoEncontradoError(
                        f"No existe un cliente con el ID "
                        f"{cliente.obtener_id()}."
                    )

        except ClienteNoEncontradoError:
            raise

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudo actualizar el cliente: {error}"
            )

        return True

    def eliminar_cliente(self, id_cliente):
        """
        Elimina un cliente por su ID.
        """

        id_cliente = Validador.validar_id(id_cliente)

        consulta = """
            DELETE FROM clientes
            WHERE id_cliente = ?
        """

        try:
            with self.__conexion() as conexion:
                cursor = conexion.execute(
                    consulta,
                    (id_cliente,)
                )

                if cursor.rowcount == 0:
                    raise ClienteNoEncontradoError(
                        f"No existe un cliente con el ID "
                        f"{id_cliente}."
                    )

        except ClienteNoEncontradoError:
            raise

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudo eliminar el cliente: {error}"
            )

        return True

    def contar_clientes(self):
        """
        Devuelve la cantidad de clientes almacenados.
        """

        consulta = """
            SELECT COUNT(*) AS cantidad
            FROM clientes
        """

        try:
            with self.__conexion() as conexion:
                fila = conexion.execute(
                    consulta
                ).fetchone()

                return fila["cantidad"]

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudo contar los clientes: {error}"
            )

    def vaciar_clientes(self):
        """
        Elimina todos los clientes de la tabla.

        Debe utilizarse solamente para pruebas.
        """

        try:
            with self.__conexion() as conexion:
                conexion.execute(
                    "DELETE FROM clientes"
                )

        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudo vaciar la tabla: {error}"
            )

        return True

    def obtener_ruta(self):
        return str(self.__ruta_base_datos)