import unittest

from pathlib import Path
from tempfile import TemporaryDirectory

from modelos.cliente_regular import ClienteRegular
from modelos.cliente_premium import ClientePremium
from modelos.cliente_corporativo import ClienteCorporativo

from servicios.base_datos import BaseDatos
from servicios.gestor_archivos import GestorArchivos
from servicios.gestor_clientes import GestorClientes
from servicios.registro_actividad import RegistroActividad

from servicios.excepciones import (
    ClienteDuplicadoError,
    EmailInvalidoError,
    RutInvalidoError,
    TipoClienteInvalidoError
)


class TestModelosClientes(unittest.TestCase):
    """
    Pruebas de las clases ClienteRegular,
    ClientePremium y ClienteCorporativo.
    """

    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        """

        self.cliente_regular = ClienteRegular(
            1,
            "María Eugenia",
            "maria@email.cl",
            "+56 9 1234 5678",
            "Viña del Mar"
        )

        self.cliente_premium = ClientePremium(
            2,
            "Ana Pérez",
            "ana@email.cl",
            "56987654321",
            "Valparaíso",
            500
        )

        self.cliente_corporativo = ClienteCorporativo(
            3,
            "Carlos Soto",
            "carlos@solutiontech.cl",
            "56955555555",
            "Santiago Centro",
            "SolutionTech",
            "76.123.456-0",
            "Carlos Soto"
        )

    def test_creacion_cliente_regular(self):
        """
        Comprueba que el cliente regular se cree
        con los datos correctos.
        """

        self.assertEqual(
            self.cliente_regular.obtener_id(),
            1
        )

        self.assertEqual(
            self.cliente_regular.obtener_nombre(),
            "María Eugenia"
        )

        self.assertEqual(
            self.cliente_regular.obtener_email(),
            "maria@email.cl"
        )

        self.assertEqual(
            self.cliente_regular.obtener_telefono(),
            "56912345678"
        )

        self.assertEqual(
            self.cliente_regular.obtener_direccion(),
            "Viña del Mar"
        )

    def test_descuentos_polimorficos(self):
        """
        Comprueba que cada tipo de cliente
        calcule un descuento diferente.
        """

        self.assertEqual(
            self.cliente_regular.calcular_descuento(),
            0
        )

        self.assertEqual(
            self.cliente_premium.calcular_descuento(),
            10
        )

        self.assertEqual(
            self.cliente_corporativo.calcular_descuento(),
            15
        )

    def test_puntos_cliente_premium(self):
        """
        Comprueba que los puntos se agreguen correctamente.
        """

        resultado = self.cliente_premium.agregar_puntos(100)

        self.assertTrue(resultado)

        self.assertEqual(
            self.cliente_premium.obtener_puntos(),
            600
        )

        self.cliente_premium.establecer_puntos(800)

        self.assertEqual(
            self.cliente_premium.obtener_puntos(),
            800
        )

    def test_conversion_diccionario(self):
        """
        Comprueba que los clientes se conviertan
        correctamente en diccionarios.
        """

        regular = (
            self.cliente_regular.convertir_a_diccionario()
        )

        premium = (
            self.cliente_premium.convertir_a_diccionario()
        )

        corporativo = (
            self.cliente_corporativo.convertir_a_diccionario()
        )

        self.assertEqual(
            regular["tipo_cliente"],
            "ClienteRegular"
        )

        self.assertEqual(
            premium["tipo_cliente"],
            "ClientePremium"
        )

        self.assertEqual(
            premium["puntos"],
            500
        )

        self.assertEqual(
            corporativo["tipo_cliente"],
            "ClienteCorporativo"
        )

        self.assertEqual(
            corporativo["empresa"],
            "SolutionTech"
        )

        self.assertEqual(
            corporativo["rut_empresa"],
            "76123456-0"
        )

    def test_comparacion_clientes(self):
        """
        Comprueba el método especial __eq__.
        Dos clientes con el mismo ID se consideran iguales.
        """

        otro_cliente = ClienteRegular(
            1,
            "Otra Persona",
            "otra@email.cl",
            "56911111111",
            "Valparaíso"
        )

        cliente_diferente = ClienteRegular(
            4,
            "Pedro Soto",
            "pedro@email.cl",
            "56922222222",
            "Quilpué"
        )

        self.assertEqual(
            self.cliente_regular,
            otro_cliente
        )

        self.assertNotEqual(
            self.cliente_regular,
            cliente_diferente
        )

    def test_email_invalido(self):
        """
        Comprueba que un correo inválido
        genere la excepción correspondiente.
        """

        with self.assertRaises(EmailInvalidoError):
            ClienteRegular(
                10,
                "Persona Prueba",
                "correo-invalido",
                "56912345678",
                "Viña del Mar"
            )

    def test_rut_invalido(self):
        """
        Comprueba que un RUT con dígito
        verificador incorrecto sea rechazado.
        """

        with self.assertRaises(RutInvalidoError):
            ClienteCorporativo(
                11,
                "Persona Empresa",
                "empresa@email.cl",
                "56912345678",
                "Santiago",
                "Empresa de Prueba",
                "76.123.456-1",
                "Persona Contacto"
            )


class TestPersistencia(unittest.TestCase):
    """
    Pruebas de SQLite, JSON, CSV y logs.
    """

    def setUp(self):
        """
        Crea una carpeta temporal para no modificar
        los datos reales del proyecto.
        """

        self.carpeta_temporal = TemporaryDirectory()

        ruta_temporal = Path(
            self.carpeta_temporal.name
        )

        self.ruta_db = (
            ruta_temporal / "clientes_prueba.db"
        )

        self.ruta_json = (
            ruta_temporal / "clientes_prueba.json"
        )

        self.ruta_csv = (
            ruta_temporal / "clientes_prueba.csv"
        )

        self.ruta_log = (
            ruta_temporal / "actividades_prueba.log"
        )

        self.base_datos = BaseDatos(
            self.ruta_db
        )

        self.gestor_archivos = GestorArchivos(
            ruta_json=self.ruta_json,
            ruta_csv=self.ruta_csv
        )

        self.registro = RegistroActividad(
            ruta_archivo=self.ruta_log
        )

        self.cliente_regular = ClienteRegular(
            1,
            "María Eugenia",
            "maria@email.cl",
            "56912345678",
            "Viña del Mar"
        )

        self.cliente_premium = ClientePremium(
            2,
            "Ana Pérez",
            "ana@email.cl",
            "56987654321",
            "Valparaíso",
            500
        )

        self.cliente_corporativo = ClienteCorporativo(
            3,
            "Carlos Soto",
            "carlos@solutiontech.cl",
            "56955555555",
            "Santiago Centro",
            "SolutionTech",
            "76.123.456-0",
            "Carlos Soto"
        )

    def tearDown(self):
        """
        Elimina los archivos temporales después de cada prueba.
        """

        self.carpeta_temporal.cleanup()

    def test_sqlite_crud(self):
        """
        Comprueba creación, lectura,
        actualización y eliminación en SQLite.
        """

        self.base_datos.guardar_cliente(
            self.cliente_regular
        )

        self.assertEqual(
            self.base_datos.contar_clientes(),
            1
        )

        cliente_encontrado = (
            self.base_datos.buscar_cliente(1)
        )

        self.assertEqual(
            cliente_encontrado.obtener_nombre(),
            "María Eugenia"
        )

        self.cliente_regular.establecer_nombre(
            "María Eugenia Perinetti"
        )

        self.base_datos.actualizar_cliente(
            self.cliente_regular
        )

        cliente_actualizado = (
            self.base_datos.buscar_cliente(1)
        )

        self.assertEqual(
            cliente_actualizado.obtener_nombre(),
            "María Eugenia Perinetti"
        )

        self.base_datos.eliminar_cliente(1)

        self.assertEqual(
            self.base_datos.contar_clientes(),
            0
        )

    def test_json_y_csv(self):
        """
        Comprueba escritura y lectura de JSON y CSV.
        """

        clientes = [
            self.cliente_regular,
            self.cliente_premium,
            self.cliente_corporativo
        ]

        ruta_json = self.gestor_archivos.guardar_json(
            clientes
        )

        ruta_csv = self.gestor_archivos.exportar_csv(
            clientes
        )

        self.assertTrue(
            Path(ruta_json).exists()
        )

        self.assertTrue(
            Path(ruta_csv).exists()
        )

        clientes_json = (
            self.gestor_archivos.cargar_json()
        )

        clientes_csv = (
            self.gestor_archivos.cargar_csv()
        )

        self.assertEqual(
            len(clientes_json),
            3
        )

        self.assertEqual(
            len(clientes_csv),
            3
        )

        self.assertIsInstance(
            clientes_json[0],
            ClienteRegular
        )

        self.assertIsInstance(
            clientes_json[1],
            ClientePremium
        )

        self.assertIsInstance(
            clientes_json[2],
            ClienteCorporativo
        )

        self.assertEqual(
            clientes_json[1].obtener_puntos(),
            500
        )

        self.assertEqual(
            clientes_csv[2].obtener_empresa(),
            "SolutionTech"
        )

    def test_registro_actividad(self):
        """
        Comprueba que una actividad sea guardada y leída.
        """

        self.registro.registrar(
            "Prueba",
            "Se ejecutó una prueba unitaria."
        )

        actividades = self.registro.leer_registros()

        self.assertEqual(
            len(actividades),
            1
        )

        self.assertIn(
            "PRUEBA",
            actividades[0]
        )

        self.assertIn(
            "Se ejecutó una prueba unitaria.",
            actividades[0]
        )


class TestGestorClientes(unittest.TestCase):
    """
    Pruebas del gestor integrado.
    """

    def setUp(self):
        """
        Crea dependencias temporales para cada prueba.
        """

        self.carpeta_temporal = TemporaryDirectory()

        ruta_temporal = Path(
            self.carpeta_temporal.name
        )

        self.base_datos = BaseDatos(
            ruta_temporal / "clientes.db"
        )

        self.gestor_archivos = GestorArchivos(
            ruta_json=(
                ruta_temporal / "clientes.json"
            ),
            ruta_csv=(
                ruta_temporal / "clientes.csv"
            )
        )

        self.registro = RegistroActividad(
            ruta_temporal / "actividades.log"
        )

        self.gestor = GestorClientes(
            base_datos=self.base_datos,
            gestor_archivos=self.gestor_archivos,
            registro_actividad=self.registro
        )

        self.cliente_regular = ClienteRegular(
            1,
            "María Eugenia",
            "maria@email.cl",
            "56912345678",
            "Viña del Mar"
        )

        self.cliente_premium = ClientePremium(
            2,
            "Ana Pérez",
            "ana@email.cl",
            "56987654321",
            "Valparaíso",
            500
        )

        self.cliente_corporativo = ClienteCorporativo(
            3,
            "Carlos Soto",
            "carlos@solutiontech.cl",
            "56955555555",
            "Santiago Centro",
            "SolutionTech",
            "76.123.456-0",
            "Carlos Soto"
        )

    def tearDown(self):
        """
        Elimina los archivos temporales.
        """

        self.carpeta_temporal.cleanup()

    def test_gestor_crud_integrado(self):
        """
        Comprueba las operaciones principales del gestor.
        """

        self.gestor.agregar_cliente(
            self.cliente_regular
        )

        self.gestor.agregar_cliente(
            self.cliente_premium
        )

        self.gestor.agregar_cliente(
            self.cliente_corporativo
        )

        self.assertEqual(
            self.gestor.obtener_cantidad_clientes(),
            3
        )

        cliente_encontrado = (
            self.gestor.buscar_cliente(2)
        )

        self.assertEqual(
            cliente_encontrado.obtener_nombre(),
            "Ana Pérez"
        )

        self.gestor.editar_cliente(
            1,
            nombre="María Eugenia Perinetti",
            email="maria.perinetti@email.cl"
        )

        cliente_actualizado = (
            self.base_datos.buscar_cliente(1)
        )

        self.assertEqual(
            cliente_actualizado.obtener_nombre(),
            "María Eugenia Perinetti"
        )

        self.gestor.eliminar_cliente(3)

        self.assertEqual(
            self.gestor.obtener_cantidad_clientes(),
            2
        )

        self.assertEqual(
            self.base_datos.contar_clientes(),
            2
        )

        rutas = self.gestor.obtener_rutas()

        self.assertTrue(
            Path(rutas["json"]).exists()
        )

        self.assertTrue(
            Path(rutas["csv"]).exists()
        )

        actividades = (
            self.gestor.leer_actividades()
        )

        self.assertGreaterEqual(
            len(actividades),
            5
        )

    def test_cliente_duplicado(self):
        """
        Comprueba que no puedan registrarse
        dos clientes con el mismo ID.
        """

        self.gestor.agregar_cliente(
            self.cliente_regular
        )

        cliente_repetido = ClienteRegular(
            1,
            "Otra Persona",
            "otra@email.cl",
            "56911111111",
            "Quilpué"
        )

        with self.assertRaises(
            ClienteDuplicadoError
        ):
            self.gestor.agregar_cliente(
                cliente_repetido
            )

    def test_agregar_puntos_cliente_premium(self):
        """
        Comprueba que el gestor agregue puntos
        y los guarde en SQLite.
        """

        self.gestor.agregar_cliente(
            self.cliente_premium
        )

        cliente = self.gestor.agregar_puntos(
            2,
            100
        )

        self.assertEqual(
            cliente.obtener_puntos(),
            600
        )

        cliente_sqlite = (
            self.base_datos.buscar_cliente(2)
        )

        self.assertEqual(
            cliente_sqlite.obtener_puntos(),
            600
        )

    def test_puntos_en_cliente_no_premium(self):
        """
        Comprueba que un cliente regular
        no pueda recibir puntos premium.
        """

        self.gestor.agregar_cliente(
            self.cliente_regular
        )

        with self.assertRaises(
            TipoClienteInvalidoError
        ):
            self.gestor.agregar_puntos(
                1,
                100
            )


if __name__ == "__main__":
    unittest.main()