class ErrorValidacion(Exception):
    """
    Excepción base para todos los errores de validación.
    """

    pass


class IdInvalidoError(ErrorValidacion):
    pass


class NombreInvalidoError(ErrorValidacion):
    pass


class EmailInvalidoError(ErrorValidacion):
    pass


class TelefonoInvalidoError(ErrorValidacion):
    pass


class DireccionInvalidaError(ErrorValidacion):
    pass


class RutInvalidoError(ErrorValidacion):
    pass


class EmpresaInvalidaError(ErrorValidacion):
    pass


class PuntosInvalidosError(ErrorValidacion):
    pass


class ErrorCliente(Exception):
    """
    Excepción base para errores relacionados con clientes.
    """

    pass


class ClienteDuplicadoError(ErrorCliente):
    pass


class ClienteNoEncontradoError(ErrorCliente):
    pass


class TipoClienteInvalidoError(ErrorCliente):
    pass


class ErrorArchivo(Exception):
    """
    Excepción base para errores relacionados con archivos.
    """

    pass


class ErrorRegistroActividad(ErrorArchivo):
    pass


class ErrorJSON(ErrorArchivo):
    pass


class ErrorCSV(ErrorArchivo):
    pass


class ErrorBaseDatos(Exception):
    """
    Excepción base para errores relacionados con SQLite.
    """

    pass


class ErrorIntegracion(Exception):
    """
    Excepción base para integraciones externas.
    """

    pass


class ErrorAPIExterna(ErrorIntegracion):
    """
    Error producido al consultar una API externa.
    """

    pass


class ErrorNotificacion(ErrorIntegracion):
    """
    Error producido al enviar una notificación.
    """

    pass