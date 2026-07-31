from modelos.cliente import Cliente


class ClienteRegular(Cliente):
    """
    Representa a un cliente regular.
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
        super().__init__(
            id_cliente,
            nombre,
            email,
            telefono,
            direccion,
            fecha_registro
        )

    def calcular_descuento(self):
        return 0

    def __str__(self):
        return (
            f"{super().__str__()} | "
            f"Tipo: Cliente regular | "
            f"Descuento: {self.calcular_descuento()}%"
        )