from datetime import datetime

from servicios.validaciones import Validador


class Cliente:
    """
    Clase padre que representa a un cliente del sistema.
    """

    def __init__(
        self,
        id_cliente,
        nombre,
        email,
        telefono,
        direccion,
        fecha_registro=None
    ):
        self.__id_cliente = Validador.validar_id(id_cliente)
        self.__nombre = Validador.validar_nombre(nombre)
        self.__email = Validador.validar_email(email)
        self.__telefono = Validador.validar_telefono(telefono)
        self.__direccion = Validador.validar_direccion(direccion)

        if fecha_registro:
            self.__fecha_registro = str(fecha_registro)
        else:
            self.__fecha_registro = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

    # GETTERS

    def obtener_id(self):
        return self.__id_cliente

    def obtener_nombre(self):
        return self.__nombre

    def obtener_email(self):
        return self.__email

    def obtener_telefono(self):
        return self.__telefono

    def obtener_direccion(self):
        return self.__direccion

    def obtener_fecha_registro(self):
        return self.__fecha_registro

    # SETTERS

    def establecer_nombre(self, nuevo_nombre):
        self.__nombre = Validador.validar_nombre(nuevo_nombre)

    def establecer_email(self, nuevo_email):
        self.__email = Validador.validar_email(nuevo_email)

    def establecer_telefono(self, nuevo_telefono):
        self.__telefono = Validador.validar_telefono(
            nuevo_telefono
        )

    def establecer_direccion(self, nueva_direccion):
        self.__direccion = Validador.validar_direccion(
            nueva_direccion
        )

    def calcular_descuento(self):
        """
        Método que será sobrescrito por las clases hijas.
        """

        return 0

    def convertir_a_diccionario(self):
        """
        Convierte el objeto en un diccionario.
        """

        return {
            "id_cliente": self.__id_cliente,
            "nombre": self.__nombre,
            "email": self.__email,
            "telefono": self.__telefono,
            "direccion": self.__direccion,
            "fecha_registro": self.__fecha_registro,
            "tipo_cliente": self.__class__.__name__,
            "descuento": self.calcular_descuento()
        }

    def __str__(self):
        return (
            f"ID: {self.__id_cliente} | "
            f"Nombre: {self.__nombre} | "
            f"Email: {self.__email} | "
            f"Teléfono: {self.__telefono} | "
            f"Dirección: {self.__direccion}"
        )

    def __eq__(self, otro_cliente):
        if not isinstance(otro_cliente, Cliente):
            return False

        return self.__id_cliente == otro_cliente.obtener_id()