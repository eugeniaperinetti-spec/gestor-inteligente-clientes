import re

from servicios.excepciones import (
    IdInvalidoError,
    NombreInvalidoError,
    EmailInvalidoError,
    TelefonoInvalidoError,
    DireccionInvalidaError,
    RutInvalidoError,
    EmpresaInvalidaError,
    PuntosInvalidosError
)


class Validador:
    """
    Clase encargada de validar los datos ingresados al sistema.
    Todos sus métodos son estáticos porque no necesita crear objetos.
    """

    @staticmethod
    def validar_id(id_cliente):
        """
        Valida que el ID sea un número entero mayor que cero.
        """

        if isinstance(id_cliente, bool):
            raise IdInvalidoError(
                "El ID debe ser un número entero."
            )

        try:
            id_cliente = int(id_cliente)

        except (ValueError, TypeError):
            raise IdInvalidoError(
                "El ID debe ser un número entero."
            )

        if id_cliente <= 0:
            raise IdInvalidoError(
                "El ID debe ser mayor que cero."
            )

        return id_cliente

    @staticmethod
    def validar_nombre(nombre):
        """
        Valida nombres de personas.
        """

        if not isinstance(nombre, str):
            raise NombreInvalidoError(
                "El nombre debe ser una cadena de texto."
            )

        nombre = nombre.strip()

        if len(nombre) < 3:
            raise NombreInvalidoError(
                "El nombre debe contener al menos 3 caracteres."
            )

        patron_nombre = r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s'-]+"

        if not re.fullmatch(patron_nombre, nombre):
            raise NombreInvalidoError(
                "El nombre solo puede contener letras, espacios, "
                "guiones y apóstrofes."
            )

        return nombre

    @staticmethod
    def validar_email(email):
        """
        Valida el formato básico de un correo electrónico.
        """

        if not isinstance(email, str):
            raise EmailInvalidoError(
                "El correo debe ser una cadena de texto."
            )

        email = email.strip().lower()

        patron_email = r"^[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron_email, email):
            raise EmailInvalidoError(
                "El correo electrónico no tiene un formato válido."
            )

        return email

    @staticmethod
    def validar_telefono(telefono):
        """
        Limpia y valida un teléfono.
        Acepta espacios, guiones y el signo +.
        """

        if telefono is None:
            raise TelefonoInvalidoError(
                "El teléfono no puede estar vacío."
            )

        telefono = str(telefono).strip()

        telefono_limpio = (
            telefono
            .replace("+", "")
            .replace(" ", "")
            .replace("-", "")
        )

        if not telefono_limpio.isdigit():
            raise TelefonoInvalidoError(
                "El teléfono solo puede contener números, "
                "espacios, guiones o el signo +."
            )

        if len(telefono_limpio) < 9 or len(telefono_limpio) > 12:
            raise TelefonoInvalidoError(
                "El teléfono debe contener entre 9 y 12 dígitos."
            )

        return telefono_limpio

    @staticmethod
    def validar_direccion(direccion):
        """
        Valida que la dirección tenga contenido suficiente.
        """

        if not isinstance(direccion, str):
            raise DireccionInvalidaError(
                "La dirección debe ser una cadena de texto."
            )

        direccion = direccion.strip()

        if len(direccion) < 5:
            raise DireccionInvalidaError(
                "La dirección debe contener al menos 5 caracteres."
            )

        return direccion

    @staticmethod
    def validar_empresa(empresa):
        """
        Valida el nombre de una empresa.
        """

        if not isinstance(empresa, str):
            raise EmpresaInvalidaError(
                "El nombre de la empresa debe ser texto."
            )

        empresa = empresa.strip()

        if len(empresa) < 2:
            raise EmpresaInvalidaError(
                "El nombre de la empresa debe contener "
                "al menos 2 caracteres."
            )

        return empresa

    @staticmethod
    def validar_puntos(puntos):
        """
        Valida que los puntos sean un número entero igual o mayor que cero.
        """

        if isinstance(puntos, bool):
            raise PuntosInvalidosError(
                "Los puntos deben ser un número entero."
            )

        try:
            puntos = int(puntos)

        except (ValueError, TypeError):
            raise PuntosInvalidosError(
                "Los puntos deben ser un número entero."
            )

        if puntos < 0:
            raise PuntosInvalidosError(
                "Los puntos no pueden ser negativos."
            )

        return puntos

    @staticmethod
    def validar_rut(rut):
        """
        Valida un RUT chileno mediante su dígito verificador.
        """

        if rut is None:
            raise RutInvalidoError(
                "El RUT no puede estar vacío."
            )

        rut = str(rut)

        rut_limpio = (
            rut
            .replace(".", "")
            .replace("-", "")
            .replace(" ", "")
            .strip()
            .upper()
        )

        if len(rut_limpio) < 8 or len(rut_limpio) > 9:
            raise RutInvalidoError(
                "El RUT no tiene una cantidad válida de caracteres."
            )

        cuerpo = rut_limpio[:-1]
        digito_verificador = rut_limpio[-1]

        if not cuerpo.isdigit():
            raise RutInvalidoError(
                "El cuerpo del RUT debe contener solo números."
            )

        if not (
            digito_verificador.isdigit()
            or digito_verificador == "K"
        ):
            raise RutInvalidoError(
                "El dígito verificador del RUT no es válido."
            )

        suma = 0
        multiplicador = 2

        for numero in reversed(cuerpo):
            suma += int(numero) * multiplicador
            multiplicador += 1

            if multiplicador == 8:
                multiplicador = 2

        resultado = 11 - (suma % 11)

        if resultado == 11:
            digito_calculado = "0"

        elif resultado == 10:
            digito_calculado = "K"

        else:
            digito_calculado = str(resultado)

        if digito_verificador != digito_calculado:
            raise RutInvalidoError(
                "El RUT ingresado no es válido."
            )

        return f"{cuerpo}-{digito_verificador}"