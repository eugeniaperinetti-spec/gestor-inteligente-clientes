import json
import os

from html import escape
from urllib import error, parse, request

from servicios.excepciones import (
    ErrorAPIExterna,
    ErrorNotificacion
)


def api_activada():
    """
    Comprueba si las integraciones reales están activadas.

    Para activarlas debe existir la variable:
    GIC_ACTIVAR_APIS=1
    """

    valor = os.getenv(
        "GIC_ACTIVAR_APIS",
        "0"
    ).strip().lower()

    return valor in {
        "1",
        "true",
        "si",
        "sí",
        "yes"
    }


class ValidadorEmailAPI:
    """
    Valida correos utilizando Abstract API.

    Sin configuración funciona en modo demostración,
    por lo que no realiza solicitudes externas.
    """

    URL_API = (
        "https://emailvalidation.abstractapi.com/v1/"
    )

    def __init__(
        self,
        api_key=None,
        timeout=10,
        activar=None
    ):
        self.__api_key = (
            api_key
            or os.getenv("ABSTRACT_EMAIL_API_KEY", "")
        ).strip()

        self.__timeout = timeout

        if activar is None:
            self.__activar = api_activada()
        else:
            self.__activar = bool(activar)

    def esta_configurado(self):
        """
        Indica si la API está activada y posee una clave.
        """

        return bool(
            self.__activar
            and self.__api_key
        )

    def validar(self, email):
        """
        Consulta la API externa y devuelve un resumen.

        No rechaza correos con estado UNKNOWN.
        Rechaza correos con formato inválido,
        desechables o marcados como UNDELIVERABLE.
        """

        if not self.esta_configurado():
            return {
                "consultado": False,
                "modo": "demostracion",
                "valido": True,
                "email": email,
                "entregabilidad": "NO CONSULTADA",
                "desechable": False,
                "sugerencia": "",
                "detalle": (
                    "La validación externa no está activada."
                )
            }

        parametros = parse.urlencode(
            {
                "api_key": self.__api_key,
                "email": email
            }
        )

        url = f"{self.URL_API}?{parametros}"

        solicitud = request.Request(
            url=url,
            method="GET",
            headers={
                "Accept": "application/json",
                "User-Agent": "GIC-Python/1.0"
            }
        )

        try:
            with request.urlopen(
                solicitud,
                timeout=self.__timeout
            ) as respuesta:
                contenido = respuesta.read().decode(
                    "utf-8"
                )

                datos = json.loads(contenido)

        except error.HTTPError as excepcion:
            detalle = excepcion.read().decode(
                "utf-8",
                errors="replace"
            )

            raise ErrorAPIExterna(
                "La API de validación rechazó la "
                f"solicitud. Código {excepcion.code}. "
                f"Detalle: {detalle}"
            )

        except error.URLError as excepcion:
            raise ErrorAPIExterna(
                "No fue posible conectarse con la API "
                f"de validación: {excepcion.reason}"
            )

        except TimeoutError:
            raise ErrorAPIExterna(
                "La API de validación tardó demasiado "
                "en responder."
            )

        except json.JSONDecodeError:
            raise ErrorAPIExterna(
                "La API de validación devolvió una "
                "respuesta que no es JSON válido."
            )

        formato_valido = (
            datos
            .get("is_valid_format", {})
            .get("value")
        )

        es_desechable = (
            datos
            .get("is_disposable_email", {})
            .get("value")
        )

        entregabilidad = datos.get(
            "deliverability",
            "UNKNOWN"
        )

        sugerencia = datos.get(
            "autocorrect",
            ""
        )

        valido = True
        motivos = []

        if formato_valido is False:
            valido = False
            motivos.append(
                "el formato fue rechazado por la API"
            )

        if es_desechable is True:
            valido = False
            motivos.append(
                "el dominio corresponde a un correo desechable"
            )

        if entregabilidad == "UNDELIVERABLE":
            valido = False
            motivos.append(
                "el correo fue marcado como no entregable"
            )

        if motivos:
            detalle = "; ".join(motivos)
        else:
            detalle = (
                "El correo superó la validación externa."
            )

        return {
            "consultado": True,
            "modo": "real",
            "valido": valido,
            "email": datos.get("email", email),
            "entregabilidad": entregabilidad,
            "desechable": bool(es_desechable),
            "sugerencia": sugerencia,
            "detalle": detalle
        }


class ServicioEmailBienvenida:
    """
    Envía un correo de bienvenida mediante Brevo.

    Sin configuración funciona en modo demostración.
    """

    URL_API = "https://api.brevo.com/v3/smtp/email"

    def __init__(
        self,
        api_key=None,
        remitente_email=None,
        remitente_nombre=None,
        timeout=10,
        activar=None
    ):
        self.__api_key = (
            api_key
            or os.getenv("BREVO_API_KEY", "")
        ).strip()

        self.__remitente_email = (
            remitente_email
            or os.getenv("BREVO_REMITENTE_EMAIL", "")
        ).strip()

        self.__remitente_nombre = (
            remitente_nombre
            or os.getenv(
                "BREVO_REMITENTE_NOMBRE",
                "Gestor Inteligente de Clientes"
            )
        ).strip()

        self.__timeout = timeout

        if activar is None:
            self.__activar = api_activada()
        else:
            self.__activar = bool(activar)

    def esta_configurado(self):
        """
        Indica si el servicio está listo para enviar.
        """

        return bool(
            self.__activar
            and self.__api_key
            and self.__remitente_email
        )

    def enviar(self, cliente):
        """
        Envía un correo al cliente registrado.

        En modo demostración no realiza una solicitud real.
        """

        if not self.esta_configurado():
            return {
                "enviado": False,
                "modo": "demostracion",
                "message_id": None,
                "detalle": (
                    "El mensaje de bienvenida fue simulado. "
                    "Brevo todavía no está configurado."
                )
            }

        nombre_seguro = escape(
            cliente.obtener_nombre()
        )

        correo_seguro = escape(
            cliente.obtener_email()
        )

        asunto = (
            "Bienvenida al Gestor Inteligente de Clientes"
        )

        contenido_texto = (
            f"Hola {cliente.obtener_nombre()},\n\n"
            "Tu registro fue realizado correctamente en "
            "el Gestor Inteligente de Clientes.\n\n"
            f"Identificador de cliente: "
            f"{cliente.obtener_id()}\n"
            f"Tipo de cliente: "
            f"{cliente.__class__.__name__}\n\n"
            "Gracias por registrarte."
        )

        contenido_html = f"""
        <html>
            <body>
                <h2>¡Bienvenido/a, {nombre_seguro}!</h2>

                <p>
                    Tu registro fue realizado correctamente
                    en el Gestor Inteligente de Clientes.
                </p>

                <p>
                    <strong>ID:</strong>
                    {cliente.obtener_id()}
                </p>

                <p>
                    <strong>Correo:</strong>
                    {correo_seguro}
                </p>

                <p>
                    <strong>Tipo:</strong>
                    {cliente.__class__.__name__}
                </p>

                <p>Gracias por registrarte.</p>
            </body>
        </html>
        """

        datos = {
            "sender": {
                "name": self.__remitente_nombre,
                "email": self.__remitente_email
            },
            "to": [
                {
                    "name": cliente.obtener_nombre(),
                    "email": cliente.obtener_email()
                }
            ],
            "subject": asunto,
            "textContent": contenido_texto,
            "htmlContent": contenido_html
        }

        cuerpo = json.dumps(
            datos,
            ensure_ascii=False
        ).encode("utf-8")

        solicitud = request.Request(
            url=self.URL_API,
            data=cuerpo,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "api-key": self.__api_key,
                "User-Agent": "GIC-Python/1.0"
            }
        )

        try:
            with request.urlopen(
                solicitud,
                timeout=self.__timeout
            ) as respuesta:
                contenido = respuesta.read().decode(
                    "utf-8"
                )

                datos_respuesta = (
                    json.loads(contenido)
                    if contenido
                    else {}
                )

                codigo = respuesta.status

        except error.HTTPError as excepcion:
            detalle = excepcion.read().decode(
                "utf-8",
                errors="replace"
            )

            raise ErrorNotificacion(
                "Brevo rechazó el envío. "
                f"Código {excepcion.code}. "
                f"Detalle: {detalle}"
            )

        except error.URLError as excepcion:
            raise ErrorNotificacion(
                "No fue posible conectarse con Brevo: "
                f"{excepcion.reason}"
            )

        except TimeoutError:
            raise ErrorNotificacion(
                "Brevo tardó demasiado en responder."
            )

        except json.JSONDecodeError:
            raise ErrorNotificacion(
                "Brevo devolvió una respuesta que "
                "no es JSON válido."
            )

        if codigo != 201:
            raise ErrorNotificacion(
                "Brevo no confirmó el envío del correo. "
                f"Código recibido: {codigo}."
            )

        return {
            "enviado": True,
            "modo": "real",
            "message_id": datos_respuesta.get(
                "messageId"
            ),
            "detalle": (
                "El correo de bienvenida fue enviado."
            )
        }