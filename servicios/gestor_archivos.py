import csv
import json
from pathlib import Path

from modelos.cliente import Cliente
from modelos.cliente_regular import ClienteRegular
from modelos.cliente_premium import ClientePremium
from modelos.cliente_corporativo import ClienteCorporativo

from servicios.excepciones import (
    ErrorArchivo,
    ErrorJSON,
    ErrorCSV,
    ErrorValidacion
)


class GestorArchivos:
    """
    Clase encargada de guardar y recuperar clientes
    utilizando archivos JSON y CSV.
    """

    CAMPOS_CSV = [
        "id_cliente",
        "nombre",
        "email",
        "telefono",
        "direccion",
        "fecha_registro",
        "tipo_cliente",
        "descuento",
        "puntos",
        "empresa",
        "rut_empresa",
        "contacto"
    ]

    def __init__(self, ruta_json=None, ruta_csv=None):
        carpeta_proyecto = Path(__file__).resolve().parent.parent
        carpeta_datos = carpeta_proyecto / "datos"

        carpeta_datos.mkdir(
            parents=True,
            exist_ok=True
        )

        if ruta_json is None:
            self.__ruta_json = carpeta_datos / "clientes.json"
        else:
            self.__ruta_json = Path(ruta_json)

        if ruta_csv is None:
            self.__ruta_csv = carpeta_datos / "clientes.csv"
        else:
            self.__ruta_csv = Path(ruta_csv)

    def __normalizar_clientes(self, clientes):
        """
        Convierte los clientes en una lista y valida
        que todos sean objetos de tipo Cliente.
        """

        if clientes is None:
            raise ErrorArchivo(
                "La lista de clientes no puede ser nula."
            )

        try:
            lista_clientes = list(clientes)

        except TypeError:
            raise ErrorArchivo(
                "Los clientes deben estar contenidos en una lista."
            )

        for cliente in lista_clientes:
            if not isinstance(cliente, Cliente):
                raise ErrorArchivo(
                    "Solo se pueden guardar objetos de tipo Cliente."
                )

        return lista_clientes

    @staticmethod
    def __crear_cliente_desde_diccionario(datos):
        """
        Reconstruye el objeto correcto según el tipo de cliente.
        """

        tipo_cliente = str(
            datos.get("tipo_cliente", "")
        ).strip()

        id_cliente = datos["id_cliente"]
        nombre = datos["nombre"]
        email = datos["email"]
        telefono = datos["telefono"]
        direccion = datos["direccion"]
        fecha_registro = datos.get("fecha_registro")

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
            puntos = datos.get("puntos", 0)

            if puntos in ("", None):
                puntos = 0

            return ClientePremium(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                puntos,
                fecha_registro
            )

        if tipo_cliente == "ClienteCorporativo":
            return ClienteCorporativo(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                datos["empresa"],
                datos["rut_empresa"],
                datos["contacto"],
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

        raise ErrorArchivo(
            f"El tipo de cliente '{tipo_cliente}' no es válido."
        )

    def guardar_json(self, clientes):
        """
        Guarda todos los clientes en formato JSON.
        """

        lista_clientes = self.__normalizar_clientes(clientes)

        datos = [
            cliente.convertir_a_diccionario()
            for cliente in lista_clientes
        ]

        try:
            with open(
                self.__ruta_json,
                "w",
                encoding="utf-8"
            ) as archivo:
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=4
                )

        except OSError as error:
            raise ErrorJSON(
                f"No se pudo guardar el archivo JSON: {error}"
            )

        return str(self.__ruta_json)

    def cargar_json(self):
        """
        Lee el archivo JSON y reconstruye los clientes.
        """

        if not self.__ruta_json.exists():
            return []

        if self.__ruta_json.stat().st_size == 0:
            return []

        try:
            with open(
                self.__ruta_json,
                "r",
                encoding="utf-8"
            ) as archivo:
                datos = json.load(archivo)

        except json.JSONDecodeError as error:
            raise ErrorJSON(
                f"El archivo JSON contiene datos inválidos: {error}"
            )

        except OSError as error:
            raise ErrorJSON(
                f"No se pudo leer el archivo JSON: {error}"
            )

        if not isinstance(datos, list):
            raise ErrorJSON(
                "El contenido del archivo JSON debe ser una lista."
            )

        clientes = []

        for numero_registro, registro in enumerate(
            datos,
            start=1
        ):
            if not isinstance(registro, dict):
                raise ErrorJSON(
                    f"El registro número {numero_registro} "
                    f"no tiene un formato válido."
                )

            try:
                cliente = self.__crear_cliente_desde_diccionario(
                    registro
                )

                clientes.append(cliente)

            except ErrorArchivo as error:
                raise ErrorJSON(
                    f"Error en el registro "
                    f"{numero_registro}: {error}"
                )

            except (
                KeyError,
                ErrorValidacion,
                ValueError,
                TypeError
            ) as error:
                raise ErrorJSON(
                    f"El registro número {numero_registro} "
                    f"contiene datos inválidos: {error}"
                )

        return clientes

    def exportar_csv(self, clientes):
        """
        Guarda todos los clientes en formato CSV.
        """

        lista_clientes = self.__normalizar_clientes(clientes)

        try:
            with open(
                self.__ruta_csv,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:
                escritor = csv.DictWriter(
                    archivo,
                    fieldnames=self.CAMPOS_CSV
                )

                escritor.writeheader()

                for cliente in lista_clientes:
                    datos = cliente.convertir_a_diccionario()

                    fila = {
                        campo: datos.get(campo, "")
                        for campo in self.CAMPOS_CSV
                    }

                    escritor.writerow(fila)

        except (OSError, csv.Error) as error:
            raise ErrorCSV(
                f"No se pudo guardar el archivo CSV: {error}"
            )

        return str(self.__ruta_csv)

    def cargar_csv(self):
        """
        Lee el archivo CSV y reconstruye los clientes.
        """

        if not self.__ruta_csv.exists():
            return []

        if self.__ruta_csv.stat().st_size == 0:
            return []

        clientes = []

        try:
            with open(
                self.__ruta_csv,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:
                lector = csv.DictReader(archivo)

                if lector.fieldnames is None:
                    return []

                for numero_registro, registro in enumerate(
                    lector,
                    start=1
                ):
                    try:
                        cliente = (
                            self.__crear_cliente_desde_diccionario(
                                registro
                            )
                        )

                        clientes.append(cliente)

                    except ErrorArchivo as error:
                        raise ErrorCSV(
                            f"Error en el registro "
                            f"{numero_registro}: {error}"
                        )

                    except (
                        KeyError,
                        ErrorValidacion,
                        ValueError,
                        TypeError
                    ) as error:
                        raise ErrorCSV(
                            f"El registro número "
                            f"{numero_registro} contiene "
                            f"datos inválidos: {error}"
                        )

        except ErrorCSV:
            raise

        except (OSError, csv.Error) as error:
            raise ErrorCSV(
                f"No se pudo leer el archivo CSV: {error}"
            )

        return clientes

    def obtener_ruta_json(self):
        return str(self.__ruta_json)

    def obtener_ruta_csv(self):
        return str(self.__ruta_csv)