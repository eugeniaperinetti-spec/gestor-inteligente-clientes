from modelos.cliente import Cliente
from servicios.validaciones import Validador


class ClienteCorporativo(Cliente):
    """
    Representa a un cliente corporativo.
    """

    def __init__(
        self,
        id_cliente,
        nombre,
        email,
        telefono,
        direccion,
        empresa,
        rut_empresa,
        contacto,
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

        self.__empresa = Validador.validar_empresa(empresa)
        self.__rut_empresa = Validador.validar_rut(rut_empresa)
        self.__contacto = Validador.validar_nombre(contacto)

    # GETTERS

    def obtener_empresa(self):
        return self.__empresa

    def obtener_rut_empresa(self):
        return self.__rut_empresa

    def obtener_contacto(self):
        return self.__contacto

    # SETTERS

    def establecer_empresa(self, nueva_empresa):
        self.__empresa = Validador.validar_empresa(
            nueva_empresa
        )

    def establecer_rut_empresa(self, nuevo_rut):
        self.__rut_empresa = Validador.validar_rut(
            nuevo_rut
        )

    def establecer_contacto(self, nuevo_contacto):
        self.__contacto = Validador.validar_nombre(
            nuevo_contacto
        )

    def calcular_descuento(self):
        return 15

    def convertir_a_diccionario(self):
        datos = super().convertir_a_diccionario()

        datos["empresa"] = self.__empresa
        datos["rut_empresa"] = self.__rut_empresa
        datos["contacto"] = self.__contacto

        return datos

    def __str__(self):
        return (
            f"{super().__str__()} | "
            f"Tipo: Cliente corporativo | "
            f"Empresa: {self.__empresa} | "
            f"RUT empresa: {self.__rut_empresa} | "
            f"Contacto: {self.__contacto} | "
            f"Descuento: {self.calcular_descuento()}%"
        )