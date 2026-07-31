import tkinter as tk

from tkinter import messagebox

from interfaz.ventana_principal import VentanaPrincipal

from servicios.excepciones import (
    ErrorValidacion,
    ErrorArchivo,
    ErrorBaseDatos
)


def main():
    """
    Inicia la aplicación gráfica.
    """

    ventana = tk.Tk()

    try:
        VentanaPrincipal(ventana)

    except (
        ErrorValidacion,
        ErrorArchivo,
        ErrorBaseDatos
    ) as error:
        messagebox.showerror(
            "No se pudo iniciar el sistema",
            str(error)
        )

        ventana.destroy()
        return

    except Exception as error:
        messagebox.showerror(
            "Error inesperado",
            str(error)
        )

        ventana.destroy()
        return

    ventana.mainloop()


if __name__ == "__main__":
    main()