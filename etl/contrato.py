"""Contrato de datos del Datawarehouse de Andina Retail Corp.

Es la única fuente de verdad del esquema estrella: nombres de tablas y columnas,
tipos, llaves y descripción. Lo usan el ETL (orden y tipos de columnas), la
validación (compara la BD contra este contrato) y el generador del diccionario
de datos (docs/diccionario_datos.md).

Si cambias algo aquí, cambia también sql/ddl/01_tablas.sql y regenera el
diccionario con:  python -m etl.generar_diccionario
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Columna:
    nombre: str
    tipo_sql: str
    descripcion: str
    pk: bool = False
    fk: str | None = None  # "Tabla.columna" referenciada
    nula: bool = False


@dataclass(frozen=True)
class Tabla:
    nombre: str
    tipo: str  # "dimension" | "hecho" | "control"
    grano: str
    columnas: tuple[Columna, ...]

    @property
    def nombres(self) -> list[str]:
        return [c.nombre for c in self.columnas]


C = Columna

DIM_MES = Tabla(
    "Dim_Mes", "dimension", "Un mes calendario (dimensión conformada con Dim_Tiempo)",
    (
        C("mes_key", "INT", "Llave AAAAMM, p. ej. 202401", pk=True),
        C("mes_numero", "TINYINT", "Número de mes, 1 a 12"),
        C("nombre_mes", "NVARCHAR(20)", "Nombre del mes en español"),
        C("trimestre", "TINYINT", "Trimestre, 1 a 4"),
        C("semestre", "TINYINT", "Semestre, 1 o 2"),
        C("anio", "SMALLINT", "Año"),
    ),
)

DIM_TIEMPO = Tabla(
    "Dim_Tiempo", "dimension", "Un día calendario",
    (
        C("tiempo_key", "INT", "Llave AAAAMMDD, p. ej. 20240131", pk=True),
        C("fecha", "DATE", "Fecha del día"),
        C("dia_semana", "NVARCHAR(10)", "Nombre del día en español (Lunes..Domingo)"),
        C("mes_numero", "TINYINT", "Número de mes, 1 a 12"),
        C("nombre_mes", "NVARCHAR(20)", "Nombre del mes en español"),
        C("trimestre", "TINYINT", "Trimestre, 1 a 4"),
        C("semestre", "TINYINT", "Semestre, 1 o 2"),
        C("anio", "SMALLINT", "Año"),
        C("mes_key", "INT", "Mes al que pertenece el día (enlace con Dim_Mes)", fk="Dim_Mes.mes_key"),
    ),
)

DIM_CLIENTE = Tabla(
    "Dim_Cliente", "dimension", "Un cliente",
    (
        C("cliente_key", "INT", "Llave sustituta", pk=True),
        C("cliente_id", "NVARCHAR(20)", "Código original del cliente (CLI-0001)"),
        C("nombre", "NVARCHAR(100)", "Nombre; solo descriptivo, NO es único"),
        C("segmento", "NVARCHAR(30)", "Segmento del Excel: Consumidor, Pyme o Corporativo"),
        C("fecha_registro", "DATE", "Fecha de registro del cliente"),
        C("segmento_cluster", "INT", "Grupo asignado por K-means (parte 3); NULL hasta que exista", nula=True),
    ),
)

DIM_PRODUCTO = Tabla(
    "Dim_Producto", "dimension", "Un producto",
    (
        C("producto_key", "INT", "Llave sustituta", pk=True),
        C("producto", "NVARCHAR(100)", "Nombre del producto"),
        C("categoria", "NVARCHAR(50)", "Categoría: Cómputo, Electrónica, Hogar o Línea Blanca"),
    ),
)

DIM_CANAL = Tabla(
    "Dim_Canal", "dimension", "Un canal de venta",
    (
        C("canal_key", "INT", "Llave sustituta", pk=True),
        C("canal", "NVARCHAR(30)", "Tienda física o E-commerce"),
    ),
)

DIM_VENDEDOR = Tabla(
    "Dim_Vendedor", "dimension", "Un equipo de venta",
    (
        C("vendedor_key", "INT", "Llave sustituta", pk=True),
        C("equipo", "NVARCHAR(50)", "Equipo que registra la venta"),
    ),
)

DIM_REGION = Tabla(
    "Dim_Region", "dimension", "Una región (dimensión con dos roles en Hecho_Ventas)",
    (
        C("region_key", "INT", "Llave sustituta", pk=True),
        C("region", "NVARCHAR(50)", "Nombre de la región"),
    ),
)

HECHO_VENTAS = Tabla(
    "Hecho_Ventas", "hecho", "Una orden de venta (cada orden tiene un solo producto)",
    (
        C("tiempo_key", "INT", "Fecha de la orden", pk=True, fk="Dim_Tiempo.tiempo_key"),
        C("cliente_key", "INT", "Cliente que compra", pk=True, fk="Dim_Cliente.cliente_key"),
        C("producto_key", "INT", "Producto vendido", pk=True, fk="Dim_Producto.producto_key"),
        C("canal_key", "INT", "Canal de la venta", pk=True, fk="Dim_Canal.canal_key"),
        C("vendedor_key", "INT", "Equipo que vende", pk=True, fk="Dim_Vendedor.vendedor_key"),
        C("region_cliente_key", "INT", "Región asignada al cliente (hoja Clientes)", pk=True, fk="Dim_Region.region_key"),
        C("region_venta_key", "INT", "Región donde se realizó la venta (hoja Ventas)", pk=True, fk="Dim_Region.region_key"),
        C("orden_id", "NVARCHAR(20)", "Dimensión degenerada: código de la orden (AR-20001)", pk=True),
        C("cantidad", "INT", "Unidades vendidas (aditiva)"),
        C("precio_unitario", "DECIMAL(12,2)", "Precio unitario en USD (no aditiva: usar total/cantidad)"),
        C("total", "DECIMAL(14,2)", "cantidad × precio_unitario en USD (aditiva)"),
    ),
)

HECHO_FINANZAS = Tabla(
    "Hecho_Finanzas_Mensual", "hecho", "Un mes de resultados financieros",
    (
        C("mes_key", "INT", "Mes del resultado", pk=True, fk="Dim_Mes.mes_key"),
        C("ingresos", "DECIMAL(14,2)", "Ingresos del mes, USD"),
        C("costo_ventas", "DECIMAL(14,2)", "Costo de ventas, USD"),
        C("gastos_operativos", "DECIMAL(14,2)", "Gastos operativos, USD"),
        C("utilidad_neta", "DECIMAL(14,2)", "ingresos − costo_ventas − gastos_operativos, USD"),
        C("flujo_caja", "DECIMAL(14,2)", "Flujo de caja del mes, USD"),
        C("inversiones_realizadas", "DECIMAL(14,2)", "Inversiones del mes, USD"),
        C("retorno_inversion", "DECIMAL(12,6)", "utilidad_neta ÷ inversiones_realizadas, como razón (0.94); no aditiva"),
    ),
)

HECHO_TRAFICO = Tabla(
    "Hecho_Trafico_Web", "hecho", "Un cliente por año",
    (
        C("cliente_key", "INT", "Cliente", pk=True, fk="Dim_Cliente.cliente_key"),
        C("region_cliente_key", "INT", "Región del cliente", fk="Dim_Region.region_key"),
        C("anio", "SMALLINT", "Dimensión degenerada: año de los totales", pk=True),
        C("visitas_web", "INT", "Visitas web del año"),
        C("conversiones_web", "INT", "Conversiones web del año"),
    ),
)

ETL_RECHAZOS = Tabla(
    "Etl_Rechazos", "control", "Una fila de origen que no se cargó",
    (
        C("rechazo_id", "INT", "Consecutivo", pk=True),
        C("hoja", "NVARCHAR(50)", "Hoja de origen"),
        C("fila_excel", "INT", "Número de fila en el Excel (1 = encabezado)"),
        C("llave_origen", "NVARCHAR(50)", "OrdenID, ClienteID o Mes de la fila", nula=True),
        C("causa", "NVARCHAR(300)", "Motivo del rechazo"),
    ),
)

ETL_OBSERVACIONES = Tabla(
    "Etl_Observaciones", "control", "Un dato cargado que requiere revisión",
    (
        C("observacion_id", "INT", "Consecutivo", pk=True),
        C("hoja", "NVARCHAR(50)", "Hoja de origen"),
        C("fila_excel", "INT", "Número de fila en el Excel (1 = encabezado)"),
        C("llave_origen", "NVARCHAR(50)", "OrdenID, ClienteID o Mes de la fila", nula=True),
        C("tipo", "NVARCHAR(50)", "Categoría de la observación"),
        C("detalle", "NVARCHAR(300)", "Descripción"),
    ),
)

# Orden de carga: dimensiones (respetando sus FK), hechos y control.
TABLAS: tuple[Tabla, ...] = (
    DIM_MES, DIM_TIEMPO, DIM_CLIENTE, DIM_PRODUCTO, DIM_CANAL, DIM_VENDEDOR, DIM_REGION,
    HECHO_VENTAS, HECHO_FINANZAS, HECHO_TRAFICO,
    ETL_RECHAZOS, ETL_OBSERVACIONES,
)
POR_NOMBRE = {t.nombre: t for t in TABLAS}
