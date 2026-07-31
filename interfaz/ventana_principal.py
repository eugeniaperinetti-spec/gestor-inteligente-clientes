import tkinter as tk

from tkinter import ttk, messagebox

from modelos.cliente_regular import ClienteRegular
from modelos.cliente_premium import ClientePremium
from modelos.cliente_corporativo import ClienteCorporativo

from servicios.gestor_clientes import GestorClientes

from servicios.excepciones import (
    ErrorValidacion,
    ErrorCliente,
    ErrorArchivo,
    ErrorBaseDatos
)


class VentanaPrincipal:
    """
    Interfaz gráfica del Gestor Inteligente de Clientes.
    """

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title(
            "Gestor Inteligente de Clientes - GIC"
        )

        self.ventana.geometry("1350x720")
        self.ventana.minsize(1100, 650)

        self.gestor = GestorClientes()

        self.id_cliente_seleccionado = None

        self.crear_variables()
        self.configurar_estilos()
        self.crear_interfaz()
        self.actualizar_tabla()

    def crear_variables(self):
        """
        Crea las variables asociadas a los campos.
        """

        self.variable_id = tk.StringVar()
        self.variable_nombre = tk.StringVar()
        self.variable_email = tk.StringVar()
        self.variable_telefono = tk.StringVar()
        self.variable_direccion = tk.StringVar()

        self.variable_tipo = tk.StringVar(
            value="Regular"
        )

        self.variable_puntos = tk.StringVar(
            value="0"
        )

        self.variable_empresa = tk.StringVar()
        self.variable_rut_empresa = tk.StringVar()
        self.variable_contacto = tk.StringVar()

        self.variable_busqueda = tk.StringVar()

        self.variable_estado = tk.StringVar(
            value="Sistema iniciado correctamente."
        )

    def configurar_estilos(self):
        """
        Configura estilos básicos de la interfaz.
        """

        estilo = ttk.Style()

        estilo.configure(
            "Titulo.TLabel",
            font=("Arial", 20, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("Arial", 12, "bold")
        )

        estilo.configure(
            "TButton",
            font=("Arial", 10),
            padding=6
        )

        estilo.configure(
            "Treeview",
            font=("Arial", 9),
            rowheight=26
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 9, "bold")
        )

    def crear_interfaz(self):
        """
        Crea todos los componentes de la ventana.
        """

        self.ventana.columnconfigure(
            0,
            weight=0
        )

        self.ventana.columnconfigure(
            1,
            weight=1
        )

        self.ventana.rowconfigure(
            1,
            weight=1
        )

        self.crear_encabezado()
        self.crear_formulario()
        self.crear_area_clientes()
        self.crear_barra_estado()

    def crear_encabezado(self):
        """
        Crea el encabezado principal.
        """

        marco_encabezado = ttk.Frame(
            self.ventana,
            padding=15
        )

        marco_encabezado.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        marco_encabezado.columnconfigure(
            0,
            weight=1
        )

        ttk.Label(
            marco_encabezado,
            text="Gestor Inteligente de Clientes",
            style="Titulo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ttk.Label(
            marco_encabezado,
            text=(
                "Administración de clientes, SQLite, "
                "JSON, CSV y registro de actividades"
            )
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 0)
        )

    def crear_formulario(self):
        """
        Crea el formulario de clientes.
        """

        self.marco_formulario = ttk.LabelFrame(
            self.ventana,
            text="Datos del cliente",
            padding=15
        )

        self.marco_formulario.grid(
            row=1,
            column=0,
            sticky="nsw",
            padx=(15, 8),
            pady=(0, 10)
        )

        self.marco_formulario.columnconfigure(
            1,
            weight=1
        )

        fila = 0

        ttk.Label(
            self.marco_formulario,
            text="ID:"
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        self.entrada_id = ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_id,
            width=32
        )

        self.entrada_id.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        ttk.Label(
            self.marco_formulario,
            text="Nombre:"
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_nombre
        ).grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        ttk.Label(
            self.marco_formulario,
            text="Correo:"
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_email
        ).grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        ttk.Label(
            self.marco_formulario,
            text="Teléfono:"
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_telefono
        ).grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        ttk.Label(
            self.marco_formulario,
            text="Dirección:"
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_direccion
        ).grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        ttk.Label(
            self.marco_formulario,
            text="Tipo:"
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        self.combo_tipo = ttk.Combobox(
            self.marco_formulario,
            textvariable=self.variable_tipo,
            values=(
                "Regular",
                "Premium",
                "Corporativo"
            ),
            state="readonly"
        )

        self.combo_tipo.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        self.combo_tipo.bind(
            "<<ComboboxSelected>>",
            self.actualizar_campos_tipo
        )

        fila += 1

        self.etiqueta_puntos = ttk.Label(
            self.marco_formulario,
            text="Puntos:"
        )

        self.etiqueta_puntos.grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        self.entrada_puntos = ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_puntos
        )

        self.entrada_puntos.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        self.etiqueta_empresa = ttk.Label(
            self.marco_formulario,
            text="Empresa:"
        )

        self.etiqueta_empresa.grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        self.entrada_empresa = ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_empresa
        )

        self.entrada_empresa.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        self.etiqueta_rut = ttk.Label(
            self.marco_formulario,
            text="RUT empresa:"
        )

        self.etiqueta_rut.grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        self.entrada_rut = ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_rut_empresa
        )

        self.entrada_rut.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        self.etiqueta_contacto = ttk.Label(
            self.marco_formulario,
            text="Contacto:"
        )

        self.etiqueta_contacto.grid(
            row=fila,
            column=0,
            sticky="w",
            pady=5
        )

        self.entrada_contacto = ttk.Entry(
            self.marco_formulario,
            textvariable=self.variable_contacto
        )

        self.entrada_contacto.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=5
        )

        fila += 1

        marco_botones = ttk.Frame(
            self.marco_formulario
        )

        marco_botones.grid(
            row=fila,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(15, 5)
        )

        marco_botones.columnconfigure(
            0,
            weight=1
        )

        marco_botones.columnconfigure(
            1,
            weight=1
        )

        ttk.Button(
            marco_botones,
            text="Registrar",
            command=self.registrar_cliente
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 4),
            pady=4
        )

        ttk.Button(
            marco_botones,
            text="Actualizar",
            command=self.actualizar_cliente
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(4, 0),
            pady=4
        )

        ttk.Button(
            marco_botones,
            text="Eliminar",
            command=self.eliminar_cliente
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 4),
            pady=4
        )

        ttk.Button(
            marco_botones,
            text="Limpiar formulario",
            command=self.limpiar_formulario
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(4, 0),
            pady=4
        )

        self.actualizar_campos_tipo()

    def crear_area_clientes(self):
        """
        Crea la tabla y herramientas de consulta.
        """

        marco_clientes = ttk.LabelFrame(
            self.ventana,
            text="Clientes registrados",
            padding=12
        )

        marco_clientes.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 15),
            pady=(0, 10)
        )

        marco_clientes.columnconfigure(
            0,
            weight=1
        )

        marco_clientes.rowconfigure(
            1,
            weight=1
        )

        marco_busqueda = ttk.Frame(
            marco_clientes
        )

        marco_busqueda.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        marco_busqueda.columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            marco_busqueda,
            text="Buscar por ID:"
        ).grid(
            row=0,
            column=0,
            padx=(0, 8)
        )

        ttk.Entry(
            marco_busqueda,
            textvariable=self.variable_busqueda
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0, 8)
        )

        ttk.Button(
            marco_busqueda,
            text="Buscar",
            command=self.buscar_cliente
        ).grid(
            row=0,
            column=2,
            padx=4
        )

        ttk.Button(
            marco_busqueda,
            text="Mostrar todos",
            command=self.actualizar_tabla
        ).grid(
            row=0,
            column=3,
            padx=4
        )

        ttk.Button(
            marco_busqueda,
            text="Exportar JSON/CSV",
            command=self.exportar_archivos
        ).grid(
            row=0,
            column=4,
            padx=4
        )

        ttk.Button(
            marco_busqueda,
            text="Ver actividades",
            command=self.mostrar_actividades
        ).grid(
            row=0,
            column=5,
            padx=(4, 0)
        )

        marco_tabla = ttk.Frame(
            marco_clientes
        )

        marco_tabla.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        marco_tabla.columnconfigure(
            0,
            weight=1
        )

        marco_tabla.rowconfigure(
            0,
            weight=1
        )

        columnas = (
            "id",
            "nombre",
            "email",
            "telefono",
            "direccion",
            "tipo",
            "detalle"
        )

        self.tabla_clientes = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        self.tabla_clientes.heading(
            "id",
            text="ID"
        )

        self.tabla_clientes.heading(
            "nombre",
            text="Nombre"
        )

        self.tabla_clientes.heading(
            "email",
            text="Correo"
        )

        self.tabla_clientes.heading(
            "telefono",
            text="Teléfono"
        )

        self.tabla_clientes.heading(
            "direccion",
            text="Dirección"
        )

        self.tabla_clientes.heading(
            "tipo",
            text="Tipo"
        )

        self.tabla_clientes.heading(
            "detalle",
            text="Información adicional"
        )

        self.tabla_clientes.column(
            "id",
            width=55,
            anchor="center"
        )

        self.tabla_clientes.column(
            "nombre",
            width=160
        )

        self.tabla_clientes.column(
            "email",
            width=190
        )

        self.tabla_clientes.column(
            "telefono",
            width=115
        )

        self.tabla_clientes.column(
            "direccion",
            width=180
        )

        self.tabla_clientes.column(
            "tipo",
            width=105,
            anchor="center"
        )

        self.tabla_clientes.column(
            "detalle",
            width=220
        )

        barra_vertical = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=self.tabla_clientes.yview
        )

        barra_horizontal = ttk.Scrollbar(
            marco_tabla,
            orient="horizontal",
            command=self.tabla_clientes.xview
        )

        self.tabla_clientes.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla_clientes.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.tabla_clientes.bind(
            "<<TreeviewSelect>>",
            self.cargar_cliente_seleccionado
        )

        self.etiqueta_cantidad = ttk.Label(
            marco_clientes,
            text="Clientes registrados: 0",
            style="Subtitulo.TLabel"
        )

        self.etiqueta_cantidad.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(10, 0)
        )

    def crear_barra_estado(self):
        """
        Crea una barra inferior de mensajes.
        """

        barra_estado = ttk.Label(
            self.ventana,
            textvariable=self.variable_estado,
            relief="sunken",
            anchor="w",
            padding=6
        )

        barra_estado.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew"
        )

    def actualizar_campos_tipo(self, evento=None):
        """
        Muestra los campos correspondientes al tipo elegido.
        """

        tipo = self.variable_tipo.get()

        self.etiqueta_puntos.grid_remove()
        self.entrada_puntos.grid_remove()

        self.etiqueta_empresa.grid_remove()
        self.entrada_empresa.grid_remove()

        self.etiqueta_rut.grid_remove()
        self.entrada_rut.grid_remove()

        self.etiqueta_contacto.grid_remove()
        self.entrada_contacto.grid_remove()

        if tipo == "Premium":
            self.etiqueta_puntos.grid()
            self.entrada_puntos.grid()

        elif tipo == "Corporativo":
            self.etiqueta_empresa.grid()
            self.entrada_empresa.grid()

            self.etiqueta_rut.grid()
            self.entrada_rut.grid()

            self.etiqueta_contacto.grid()
            self.entrada_contacto.grid()

    def crear_cliente_desde_formulario(self):
        """
        Crea el tipo de cliente seleccionado.
        """

        id_cliente = self.variable_id.get()
        nombre = self.variable_nombre.get()
        email = self.variable_email.get()
        telefono = self.variable_telefono.get()
        direccion = self.variable_direccion.get()
        tipo = self.variable_tipo.get()

        if tipo == "Regular":
            return ClienteRegular(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion
            )

        if tipo == "Premium":
            return ClientePremium(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                self.variable_puntos.get()
            )

        if tipo == "Corporativo":
            return ClienteCorporativo(
                id_cliente,
                nombre,
                email,
                telefono,
                direccion,
                self.variable_empresa.get(),
                self.variable_rut_empresa.get(),
                self.variable_contacto.get()
            )

        raise ValueError(
            "El tipo de cliente no es válido."
        )

    def registrar_cliente(self):
        """
        Registra un cliente nuevo.
        """

        try:
            cliente = self.crear_cliente_desde_formulario()

            self.gestor.agregar_cliente(cliente)

            self.actualizar_tabla()
            self.limpiar_formulario()

            self.variable_estado.set(
                f"Cliente ID {cliente.obtener_id()} "
                f"registrado correctamente."
            )

            messagebox.showinfo(
                "Registro exitoso",
                "El cliente fue registrado correctamente."
            )

        except (
            ErrorValidacion,
            ErrorCliente,
            ErrorArchivo,
            ErrorBaseDatos
        ) as error:
            messagebox.showerror(
                "No se pudo registrar",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    def actualizar_cliente(self):
        """
        Actualiza el cliente seleccionado.
        """

        if self.id_cliente_seleccionado is None:
            messagebox.showwarning(
                "Cliente no seleccionado",
                "Selecciona un cliente de la tabla."
            )
            return

        try:
            tipo = self.variable_tipo.get()

            puntos = None
            empresa = None
            rut_empresa = None
            contacto = None

            if tipo == "Premium":
                puntos = self.variable_puntos.get()

            elif tipo == "Corporativo":
                empresa = self.variable_empresa.get()
                rut_empresa = self.variable_rut_empresa.get()
                contacto = self.variable_contacto.get()

            cliente = self.gestor.editar_cliente(
                id_cliente=self.id_cliente_seleccionado,
                nombre=self.variable_nombre.get(),
                email=self.variable_email.get(),
                telefono=self.variable_telefono.get(),
                direccion=self.variable_direccion.get(),
                puntos=puntos,
                empresa=empresa,
                rut_empresa=rut_empresa,
                contacto=contacto
            )

            self.actualizar_tabla()
            self.limpiar_formulario()

            self.variable_estado.set(
                f"Cliente ID {cliente.obtener_id()} "
                f"actualizado correctamente."
            )

            messagebox.showinfo(
                "Actualización exitosa",
                "Los datos fueron actualizados."
            )

        except (
            ErrorValidacion,
            ErrorCliente,
            ErrorArchivo,
            ErrorBaseDatos
        ) as error:
            messagebox.showerror(
                "No se pudo actualizar",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    def eliminar_cliente(self):
        """
        Elimina el cliente seleccionado.
        """

        if self.id_cliente_seleccionado is None:
            messagebox.showwarning(
                "Cliente no seleccionado",
                "Selecciona un cliente de la tabla."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            (
                f"¿Deseas eliminar al cliente con ID "
                f"{self.id_cliente_seleccionado}?"
            )
        )

        if not confirmar:
            return

        try:
            cliente = self.gestor.eliminar_cliente(
                self.id_cliente_seleccionado
            )

            self.actualizar_tabla()
            self.limpiar_formulario()

            self.variable_estado.set(
                f"Cliente ID {cliente.obtener_id()} eliminado."
            )

            messagebox.showinfo(
                "Cliente eliminado",
                "El cliente fue eliminado correctamente."
            )

        except (
            ErrorValidacion,
            ErrorCliente,
            ErrorArchivo,
            ErrorBaseDatos
        ) as error:
            messagebox.showerror(
                "No se pudo eliminar",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    def obtener_detalle_cliente(self, cliente):
        """
        Genera el texto adicional de cada tipo.
        """

        if isinstance(cliente, ClientePremium):
            return (
                f"Puntos: {cliente.obtener_puntos()} | "
                f"Descuento: "
                f"{cliente.calcular_descuento()}%"
            )

        if isinstance(cliente, ClienteCorporativo):
            return (
                f"{cliente.obtener_empresa()} | "
                f"RUT: {cliente.obtener_rut_empresa()}"
            )

        return (
            f"Descuento: "
            f"{cliente.calcular_descuento()}%"
        )

    def obtener_nombre_tipo(self, cliente):
        """
        Devuelve un nombre simple para el tipo.
        """

        if isinstance(cliente, ClientePremium):
            return "Premium"

        if isinstance(cliente, ClienteCorporativo):
            return "Corporativo"

        return "Regular"

    def actualizar_tabla(self):
        """
        Carga todos los clientes en la tabla.
        """

        for elemento in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(elemento)

        clientes = self.gestor.listar_clientes()

        for cliente in clientes:
            self.tabla_clientes.insert(
                "",
                "end",
                values=(
                    cliente.obtener_id(),
                    cliente.obtener_nombre(),
                    cliente.obtener_email(),
                    cliente.obtener_telefono(),
                    cliente.obtener_direccion(),
                    self.obtener_nombre_tipo(cliente),
                    self.obtener_detalle_cliente(cliente)
                )
            )

        self.etiqueta_cantidad.config(
            text=(
                f"Clientes registrados: "
                f"{len(clientes)}"
            )
        )

        self.variable_estado.set(
            f"Se muestran {len(clientes)} clientes."
        )

    def cargar_cliente_seleccionado(self, evento=None):
        """
        Carga en el formulario el cliente seleccionado.
        """

        seleccion = self.tabla_clientes.selection()

        if not seleccion:
            return

        elemento = seleccion[0]

        valores = self.tabla_clientes.item(
            elemento,
            "values"
        )

        if not valores:
            return

        id_cliente = valores[0]

        try:
            cliente = self.gestor.buscar_cliente(
                id_cliente
            )

        except (
            ErrorValidacion,
            ErrorCliente
        ):
            return

        self.id_cliente_seleccionado = (
            cliente.obtener_id()
        )

        self.variable_id.set(
            cliente.obtener_id()
        )

        self.variable_nombre.set(
            cliente.obtener_nombre()
        )

        self.variable_email.set(
            cliente.obtener_email()
        )

        self.variable_telefono.set(
            cliente.obtener_telefono()
        )

        self.variable_direccion.set(
            cliente.obtener_direccion()
        )

        self.entrada_id.config(
            state="disabled"
        )

        self.combo_tipo.config(
            state="disabled"
        )

        if isinstance(cliente, ClientePremium):
            self.variable_tipo.set("Premium")

            self.variable_puntos.set(
                cliente.obtener_puntos()
            )

        elif isinstance(cliente, ClienteCorporativo):
            self.variable_tipo.set("Corporativo")

            self.variable_empresa.set(
                cliente.obtener_empresa()
            )

            self.variable_rut_empresa.set(
                cliente.obtener_rut_empresa()
            )

            self.variable_contacto.set(
                cliente.obtener_contacto()
            )

        else:
            self.variable_tipo.set("Regular")

        self.actualizar_campos_tipo()

        self.variable_estado.set(
            f"Cliente ID {cliente.obtener_id()} seleccionado."
        )

    def limpiar_formulario(self):
        """
        Limpia el formulario y habilita ID y tipo.
        """

        self.id_cliente_seleccionado = None

        self.variable_id.set("")
        self.variable_nombre.set("")
        self.variable_email.set("")
        self.variable_telefono.set("")
        self.variable_direccion.set("")

        self.variable_tipo.set("Regular")
        self.variable_puntos.set("0")

        self.variable_empresa.set("")
        self.variable_rut_empresa.set("")
        self.variable_contacto.set("")

        self.entrada_id.config(
            state="normal"
        )

        self.combo_tipo.config(
            state="readonly"
        )

        self.actualizar_campos_tipo()

        for elemento in self.tabla_clientes.selection():
            self.tabla_clientes.selection_remove(
                elemento
            )

        self.entrada_id.focus()

        self.variable_estado.set(
            "Formulario preparado para un nuevo cliente."
        )

    def buscar_cliente(self):
        """
        Busca un cliente y lo selecciona en la tabla.
        """

        id_cliente = self.variable_busqueda.get()

        try:
            cliente = self.gestor.buscar_cliente(
                id_cliente
            )

            self.actualizar_tabla()

            for elemento in self.tabla_clientes.get_children():
                valores = self.tabla_clientes.item(
                    elemento,
                    "values"
                )

                if str(valores[0]) == str(
                    cliente.obtener_id()
                ):
                    self.tabla_clientes.selection_set(
                        elemento
                    )

                    self.tabla_clientes.focus(
                        elemento
                    )

                    self.tabla_clientes.see(
                        elemento
                    )

                    self.cargar_cliente_seleccionado()
                    break

            self.variable_estado.set(
                f"Cliente ID {cliente.obtener_id()} encontrado."
            )

        except (
            ErrorValidacion,
            ErrorCliente
        ) as error:
            messagebox.showerror(
                "Cliente no encontrado",
                str(error)
            )

    def exportar_archivos(self):
        """
        Actualiza los archivos JSON y CSV.
        """

        try:
            rutas = self.gestor.exportar_archivos()

            self.variable_estado.set(
                "Archivos JSON y CSV actualizados."
            )

            messagebox.showinfo(
                "Exportación completada",
                (
                    "Los archivos fueron actualizados.\n\n"
                    f"JSON:\n{rutas['json']}\n\n"
                    f"CSV:\n{rutas['csv']}"
                )
            )

        except (
            ErrorArchivo,
            ErrorBaseDatos
        ) as error:
            messagebox.showerror(
                "Error de exportación",
                str(error)
            )

    def mostrar_actividades(self):
        """
        Abre una ventana con las actividades registradas.
        """

        try:
            actividades = self.gestor.leer_actividades()

        except ErrorArchivo as error:
            messagebox.showerror(
                "Error al leer actividades",
                str(error)
            )
            return

        ventana_actividades = tk.Toplevel(
            self.ventana
        )

        ventana_actividades.title(
            "Registro de actividades"
        )

        ventana_actividades.geometry(
            "900x500"
        )

        ventana_actividades.minsize(
            650,
            350
        )

        ventana_actividades.columnconfigure(
            0,
            weight=1
        )

        ventana_actividades.rowconfigure(
            0,
            weight=1
        )

        marco_texto = ttk.Frame(
            ventana_actividades,
            padding=12
        )

        marco_texto.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        marco_texto.columnconfigure(
            0,
            weight=1
        )

        marco_texto.rowconfigure(
            0,
            weight=1
        )

        texto = tk.Text(
            marco_texto,
            wrap="word",
            font=("Consolas", 10)
        )

        barra = ttk.Scrollbar(
            marco_texto,
            orient="vertical",
            command=texto.yview
        )

        texto.configure(
            yscrollcommand=barra.set
        )

        texto.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        barra.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        if actividades:
            texto.insert(
                "1.0",
                "\n".join(actividades)
            )

        else:
            texto.insert(
                "1.0",
                "No hay actividades registradas."
            )

        texto.config(
            state="disabled"
        )

        ttk.Button(
            ventana_actividades,
            text="Cerrar",
            command=ventana_actividades.destroy
        ).grid(
            row=1,
            column=0,
            pady=(0, 12)
        )