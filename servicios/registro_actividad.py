from datetime import datetime
from pathlib import Path

from servicios.excepciones import ErrorRegistroActividad


class RegistroActividad:
    """
    Clase encargada de guardar las operaciones
    realizadas en el sistema.
    """

    def __init__(self, ruta_archivo=None):
        if ruta_archivo is None:
            carpeta_proyecto = Path(__file__).resolve().parent.parent

            self.__ruta_archivo = (
                carpeta_proyecto
                / "datos"
                / "actividades.log"
            )
        else:
            self.__ruta_archivo = Path(ruta_archivo)

        self.__preparar_archivo()

    def __preparar_archivo(self):
        """
        Crea la carpeta y el archivo si todavía no existen.
        """

        try:
            self.__ruta_archivo.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self.__ruta_archivo.touch(exist_ok=True)

        except OSError as error:
            raise ErrorRegistroActividad(
                f"No se pudo preparar el archivo de actividades: "
                f"{error}"
            )

    def registrar(self, accion, detalle):
        """
        Agrega una nueva actividad al final del archivo.
        """

        accion = str(accion).strip().upper()
        detalle = str(detalle).strip()

        if not accion:
            raise ErrorRegistroActividad(
                "La acción del registro no puede estar vacía."
            )

        if not detalle:
            raise ErrorRegistroActividad(
                "El detalle del registro no puede estar vacío."
            )

        fecha_hora = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        linea = (
            f"[{fecha_hora}] "
            f"{accion} | "
            f"{detalle}\n"
        )

        try:
            with open(
                self.__ruta_archivo,
                "a",
                encoding="utf-8"
            ) as archivo:
                archivo.write(linea)

        except OSError as error:
            raise ErrorRegistroActividad(
                f"No se pudo guardar la actividad: {error}"
            )

        return linea.strip()

    def leer_registros(self):
        """
        Lee y devuelve todas las actividades guardadas.
        """

        try:
            with open(
                self.__ruta_archivo,
                "r",
                encoding="utf-8"
            ) as archivo:
                return [
                    linea.rstrip("\n")
                    for linea in archivo
                ]

        except FileNotFoundError:
            return []

        except OSError as error:
            raise ErrorRegistroActividad(
                f"No se pudo leer el registro de actividades: "
                f"{error}"
            )

    def limpiar_registro(self):
        """
        Elimina el contenido del archivo de actividades.
        No elimina el archivo.
        """

        try:
            with open(
                self.__ruta_archivo,
                "w",
                encoding="utf-8"
            ):
                pass

        except OSError as error:
            raise ErrorRegistroActividad(
                f"No se pudo limpiar el registro: {error}"
            )

        return True

    def obtener_ruta(self):
        """
        Devuelve la ubicación del archivo de actividades.
        """

        return str(self.__ruta_archivo)