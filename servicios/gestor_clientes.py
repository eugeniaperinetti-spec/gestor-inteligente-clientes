from modelos.cliente import Cliente
from modelos.cliente_premium import ClientePremium
from modelos.cliente_corporativo import ClienteCorporativo

from servicios.base_datos import BaseDatos
from servicios.gestor_archivos import GestorArchivos
from servicios.registro_actividad import RegistroActividad
from servicios.validaciones import Validador

from servicios.integraciones import (
    ValidadorEmailAPI,
    ServicioEmailBienvenida
)

from servicios.excepciones import (
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    TipoClienteInvalidoError,
    EmailInvalidoError,
    ErrorAPIExterna,
    ErrorNotificacion
)


class GestorClientes:
    """
    Integra la gestión de clientes con SQLite,
    JSON, CSV, logs y servicios externos.
    """

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

        self.__validador_email_api = (
            validador_email_api
            if validador_email_api is not None
            else ValidadorEmailAPI()
        )

        self.__servicio_email = (
            servicio_email
            if servicio_email is not None
            else ServicioEmailBienvenida()
        )

        self.__clientes = (
            self.__base_datos.obtener_clientes()
        )

    def __sincronizar_archivos(self):
        """
        Actualiza automáticamente JSON y CSV.
        """

        ruta_json = self.__gestor_archivos.guardar_json(
            self.__clientes
        )

        ruta_csv = self.__gestor_archivos.exportar_csv(
            self.__clientes
        )

        return {
            "json": ruta_json,
            "csv": ruta_csv
        }

    def __validar_email_externo(self, cliente):
        """
        Valida el correo mediante la API externa.

        Cuando la API no está configurada,
        continúa en modo demostración.
        """

        try:
            resultado = (
                self.__validador_email_api.validar(
                    cliente.obtener_email()
                )
            )

        except ErrorAPIExterna as error:
            return {
                "consultado": False,
                "modo": "error",
                "valido": True,
                "email": cliente.obtener_email(),
                "entregabilidad": "NO CONSULTADA",
                "desechable": False,
                "sugerencia": "",
                "detalle": str(error)
            }

        if (
            resultado["consultado"]
            and not resultado["valido"]
        ):
            mensaje = resultado["detalle"]

            if resultado.get("sugerencia"):
                mensaje += (
                    ". Sugerencia: "
                    f"{resultado['sugerencia']}"
                )

            raise EmailInvalidoError(
                "La validación externa rechazó el correo: "
                f"{mensaje}"
            )

        return resultado

    def __enviar_bienvenida(self, cliente):
        """
        Intenta enviar el mensaje de bienvenida.

        Un fallo de notificación no elimina al cliente
        que ya fue registrado.
        """

        try:
            return self.__servicio_email.enviar(
                cliente
            )

        except ErrorNotificacion as error:
            return {
                "enviado": False,
                "modo": "error",
                "message_id": None,
                "detalle": str(error)
            }

    def agregar_cliente(self, cliente):
        """
        Guarda el cliente y ejecuta las integraciones.
        """

        if not isinstance(cliente, Cliente):
            raise TipoClienteInvalidoError(
                "Solo se pueden registrar objetos "
                "de tipo Cliente."
            )

        if self.existe_cliente(cliente.obtener_id()):
            raise ClienteDuplicadoError(
                f"Ya existe un cliente con el ID "
                f"{cliente.obtener_id()}."
            )

        resultado_validacion = (
            self.__validar_email_externo(cliente)
        )

        self.__base_datos.guardar_cliente(cliente)

        self.__clientes.append(cliente)

        self.__sincronizar_archivos()

        self.__registro_actividad.registrar(
            "Creación",
            (
                f"Se registró el cliente "
                f"ID {cliente.obtener_id()}, "
                f"nombre {cliente.obtener_nombre()}, "
                f"tipo {cliente.__class__.__name__}."
            )
        )

        if resultado_validacion["consultado"]:
            self.__registro_actividad.registrar(
                "Validación API",
                (
                    f"Correo del cliente ID "
                    f"{cliente.obtener_id()} validado. "
                    f"Entregabilidad: "
                    f"{resultado_validacion['entregabilidad']}."
                )
            )

        elif resultado_validacion["modo"] == "error":
            self.__registro_actividad.registrar(
                "Advertencia API",
                (
                    f"No se pudo consultar la API para "
                    f"el cliente ID {cliente.obtener_id()}. "
                    f"{resultado_validacion['detalle']}"
                )
            )

        else:
            self.__registro_actividad.registrar(
                "Validación demostración",
                (
                    f"El correo del cliente ID "
                    f"{cliente.obtener_id()} fue validado "
                    f"solo con las reglas locales."
                )
            )

        resultado_notificacion = (
            self.__enviar_bienvenida(cliente)
        )

        if resultado_notificacion["enviado"]:
            self.__registro_actividad.registrar(
                "Notificación",
                (
                    f"Se envió el correo de bienvenida "
                    f"al cliente ID {cliente.obtener_id()}. "
                    f"Message ID: "
                    f"{resultado_notificacion['message_id']}."
                )
            )

        elif resultado_notificacion["modo"] == "error":
            self.__registro_actividad.registrar(
                "Error notificación",
                (
                    f"No se pudo enviar el correo al "
                    f"cliente ID {cliente.obtener_id()}. "
                    f"{resultado_notificacion['detalle']}"
                )
            )

        else:
            self.__registro_actividad.registrar(
                "Notificación demostración",
                (
                    f"Se simuló el correo de bienvenida "
                    f"para el cliente ID "
                    f"{cliente.obtener_id()}."
                )
            )

        return cliente

    def listar_clientes(self):
        return self.__clientes.copy()

    def buscar_cliente(self, id_cliente):
        id_cliente = Validador.validar_id(
            id_cliente
        )

        for cliente in self.__clientes:
            if cliente.obtener_id() == id_cliente:
                return cliente

        raise ClienteNoEncontradoError(
            f"No se encontró un cliente con el ID "
            f"{id_cliente}."
        )

    def editar_cliente(
        self,
        id_cliente,
        nombre=None,
        email=None,
        telefono=None,
        direccion=None,
        puntos=None,
        empresa=None,
        rut_empresa=None,
        contacto=None
    ):
        cliente = self.buscar_cliente(
            id_cliente
        )

        campos_modificados = []

        nombre_validado = None
        email_validado = None
        telefono_validado = None
        direccion_validada = None
        puntos_validados = None
        empresa_validada = None
        rut_validado = None
        contacto_validado = None

        if nombre is not None:
            nombre_validado = (
                Validador.validar_nombre(nombre)
            )

        if email is not None:
            email_validado = (
                Validador.validar_email(email)
            )

        if telefono is not None:
            telefono_validado = (
                Validador.validar_telefono(telefono)
            )

        if direccion is not None:
            direccion_validada = (
                Validador.validar_direccion(direccion)
            )

        if puntos is not None:
            if not isinstance(
                cliente,
                ClientePremium
            ):
                raise TipoClienteInvalidoError(
                    "Solo los clientes premium "
                    "tienen puntos."
                )

            puntos_validados = (
                Validador.validar_puntos(puntos)
            )

        if (
            empresa is not None
            or rut_empresa is not None
            or contacto is not None
        ):
            if not isinstance(
                cliente,
                ClienteCorporativo
            ):
                raise TipoClienteInvalidoError(
                    "Estos datos solo corresponden "
                    "a clientes corporativos."
                )

            if empresa is not None:
                empresa_validada = (
                    Validador.validar_empresa(
                        empresa
                    )
                )

            if rut_empresa is not None:
                rut_validado = (
                    Validador.validar_rut(
                        rut_empresa
                    )
                )

            if contacto is not None:
                contacto_validado = (
                    Validador.validar_nombre(
                        contacto
                    )
                )

        if email_validado is not None:
            resultado_email = (
                self.__validador_email_api.validar(
                    email_validado
                )
            )

            if (
                resultado_email["consultado"]
                and not resultado_email["valido"]
            ):
                raise EmailInvalidoError(
                    "La validación externa rechazó "
                    f"el correo: "
                    f"{resultado_email['detalle']}"
                )

        if nombre_validado is not None:
            cliente.establecer_nombre(
                nombre_validado
            )
            campos_modificados.append("nombre")

        if email_validado is not None:
            cliente.establecer_email(
                email_validado
            )
            campos_modificados.append("email")

        if telefono_validado is not None:
            cliente.establecer_telefono(
                telefono_validado
            )
            campos_modificados.append("teléfono")

        if direccion_validada is not None:
            cliente.establecer_direccion(
                direccion_validada
            )
            campos_modificados.append("dirección")

        if puntos_validados is not None:
            cliente.establecer_puntos(
                puntos_validados
            )
            campos_modificados.append("puntos")

        if empresa_validada is not None:
            cliente.establecer_empresa(
                empresa_validada
            )
            campos_modificados.append("empresa")

        if rut_validado is not None:
            cliente.establecer_rut_empresa(
                rut_validado
            )
            campos_modificados.append(
                "RUT empresa"
            )

        if contacto_validado is not None:
            cliente.establecer_contacto(
                contacto_validado
            )
            campos_modificados.append("contacto")

        if not campos_modificados:
            return cliente

        self.__base_datos.actualizar_cliente(
            cliente
        )

        self.__sincronizar_archivos()

        self.__registro_actividad.registrar(
            "Edición",
            (
                f"Se modificó el cliente "
                f"ID {cliente.obtener_id()}. "
                f"Campos actualizados: "
                f"{', '.join(campos_modificados)}."
            )
        )

        return cliente

    def eliminar_cliente(self, id_cliente):
        cliente = self.buscar_cliente(
            id_cliente
        )

        self.__base_datos.eliminar_cliente(
            cliente.obtener_id()
        )

        self.__clientes.remove(cliente)

        self.__sincronizar_archivos()

        self.__registro_actividad.registrar(
            "Eliminación",
            (
                f"Se eliminó el cliente "
                f"ID {cliente.obtener_id()}, "
                f"nombre {cliente.obtener_nombre()}, "
                f"tipo {cliente.__class__.__name__}."
            )
        )

        return cliente

    def agregar_puntos(
        self,
        id_cliente,
        cantidad
    ):
        cliente = self.buscar_cliente(
            id_cliente
        )

        if not isinstance(
            cliente,
            ClientePremium
        ):
            raise TipoClienteInvalidoError(
                "El cliente seleccionado "
                "no es premium."
            )

        cliente.agregar_puntos(cantidad)

        self.__base_datos.actualizar_cliente(
            cliente
        )

        self.__sincronizar_archivos()

        self.__registro_actividad.registrar(
            "Puntos",
            (
                f"Se agregaron {cantidad} puntos "
                f"al cliente ID "
                f"{cliente.obtener_id()}. "
                f"Total actual: "
                f"{cliente.obtener_puntos()}."
            )
        )

        return cliente

    def obtener_cantidad_clientes(self):
        return len(self.__clientes)

    def existe_cliente(self, id_cliente):
        try:
            id_cliente = Validador.validar_id(
                id_cliente
            )

        except Exception:
            return False

        return any(
            cliente.obtener_id() == id_cliente
            for cliente in self.__clientes
        )

    def exportar_archivos(self):
        rutas = self.__sincronizar_archivos()

        self.__registro_actividad.registrar(
            "Exportación",
            "Se actualizaron los archivos JSON y CSV."
        )

        return rutas

    def recargar_desde_base_datos(self):
        self.__clientes = (
            self.__base_datos.obtener_clientes()
        )

        return self.listar_clientes()

    def leer_actividades(self):
        return (
            self.__registro_actividad.leer_registros()
        )

    def obtener_estado_integraciones(self):
        """
        Informa si los servicios reales están configurados.
        """

        return {
            "validacion_email": (
                self.__validador_email_api.esta_configurado()
            ),
            "correo_bienvenida": (
                self.__servicio_email.esta_configurado()
            )
        }

    def obtener_rutas(self):
        return {
            "base_datos": (
                self.__base_datos.obtener_ruta()
            ),
            "json": (
                self.__gestor_archivos.obtener_ruta_json()
            ),
            "csv": (
                self.__gestor_archivos.obtener_ruta_csv()
            ),
            "registro": (
                self.__registro_actividad.obtener_ruta()
            )
        }