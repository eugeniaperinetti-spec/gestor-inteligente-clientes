from modelos.cliente import Cliente
from servicios.validaciones import Validador


class ClientePremium(Cliente):
    """
    Representa a un cliente premium.

    Tiene puntos acumulados y un descuento del 10%.
    """

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

    def obtener_puntos(self):
        return self.__puntos

    def establecer_puntos(self, nuevos_puntos):
        """
        Reemplaza la cantidad actual de puntos.
        """

        self.__puntos = Validador.validar_puntos(
            nuevos_puntos
        )

    def agregar_puntos(self, cantidad):
        """
        Agrega puntos a la cantidad existente.
        """

        cantidad = Validador.validar_puntos(cantidad)

        if cantidad == 0:
            return False

        self.__puntos += cantidad
        return True

    def calcular_descuento(self):
        return 10

    def convertir_a_diccionario(self):
        datos = super().convertir_a_diccionario()
        datos["puntos"] = self.__puntos

        return datos

    def __str__(self):
        return (
            f"{super().__str__()} | "
            f"Tipo: Cliente premium | "
            f"Puntos: {self.__puntos} | "
            f"Descuento: {self.calcular_descuento()}%"
        )