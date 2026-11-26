# Diccionario de datos

> Generado por `python -m etl.generar` desde `etl/contrato.py`. No editar a mano.

Convenciones: **PK** llave primaria, **FK** llave foránea, montos en USD. Diagrama y relaciones: [esquema_estrella.md](esquema_estrella.md).

## Dim_Mes

*Tipo:* dimension · *Grano:* Un mes calendario (dimensión conformada con Dim_Tiempo)

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `mes_key` | INT | no | PK | Llave AAAAMM, p. ej. 202401 |
| `mes_numero` | TINYINT | no |  | Número de mes, 1 a 12 |
| `nombre_mes` | NVARCHAR(20) | no |  | Nombre del mes en español |
| `trimestre` | TINYINT | no |  | Trimestre, 1 a 4 |
| `semestre` | TINYINT | no |  | Semestre, 1 o 2 |
| `anio` | SMALLINT | no |  | Año |

## Dim_Tiempo

*Tipo:* dimension · *Grano:* Un día calendario

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `tiempo_key` | INT | no | PK | Llave AAAAMMDD, p. ej. 20240131 |
| `fecha` | DATE | no |  | Fecha del día |
| `dia_semana` | NVARCHAR(10) | no |  | Nombre del día en español (Lunes..Domingo) |
| `mes_numero` | TINYINT | no |  | Número de mes, 1 a 12 |
| `nombre_mes` | NVARCHAR(20) | no |  | Nombre del mes en español |
| `trimestre` | TINYINT | no |  | Trimestre, 1 a 4 |
| `semestre` | TINYINT | no |  | Semestre, 1 o 2 |
| `anio` | SMALLINT | no |  | Año |
| `mes_key` | INT | no | FK → Dim_Mes.mes_key | Mes al que pertenece el día (enlace con Dim_Mes) |

## Dim_Cliente

*Tipo:* dimension · *Grano:* Un cliente

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `cliente_key` | INT | no | PK | Llave sustituta |
| `cliente_id` | NVARCHAR(20) | no |  | Código original del cliente (CLI-0001) |
| `nombre` | NVARCHAR(100) | no |  | Nombre; solo descriptivo, NO es único |
| `segmento` | NVARCHAR(30) | no |  | Segmento del Excel: Consumidor, Pyme o Corporativo |
| `fecha_registro` | DATE | no |  | Fecha de registro del cliente |
| `segmento_cluster` | INT | sí |  | Grupo asignado por K-means (parte 3); NULL hasta que exista |

## Dim_Producto

*Tipo:* dimension · *Grano:* Un producto

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `producto_key` | INT | no | PK | Llave sustituta |
| `producto` | NVARCHAR(100) | no |  | Nombre del producto |
| `categoria` | NVARCHAR(50) | no |  | Categoría: Cómputo, Electrónica, Hogar o Línea Blanca |

## Dim_Canal

*Tipo:* dimension · *Grano:* Un canal de venta

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `canal_key` | INT | no | PK | Llave sustituta |
| `canal` | NVARCHAR(30) | no |  | Tienda física o E-commerce |

## Dim_Vendedor

*Tipo:* dimension · *Grano:* Un equipo de venta

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `vendedor_key` | INT | no | PK | Llave sustituta |
| `equipo` | NVARCHAR(50) | no |  | Equipo que registra la venta |

## Dim_Region

*Tipo:* dimension · *Grano:* Una región (dimensión con dos roles en Hecho_Ventas)

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `region_key` | INT | no | PK | Llave sustituta |
| `region` | NVARCHAR(50) | no |  | Nombre de la región |

## Hecho_Ventas

*Tipo:* hecho · *Grano:* Una orden de venta (cada orden tiene un solo producto)

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `tiempo_key` | INT | no | PK FK → Dim_Tiempo.tiempo_key | Fecha de la orden |
| `cliente_key` | INT | no | PK FK → Dim_Cliente.cliente_key | Cliente que compra |
| `producto_key` | INT | no | PK FK → Dim_Producto.producto_key | Producto vendido |
| `canal_key` | INT | no | PK FK → Dim_Canal.canal_key | Canal de la venta |
| `vendedor_key` | INT | no | PK FK → Dim_Vendedor.vendedor_key | Equipo que vende |
| `region_cliente_key` | INT | no | PK FK → Dim_Region.region_key | Región asignada al cliente (hoja Clientes) |
| `region_venta_key` | INT | no | PK FK → Dim_Region.region_key | Región donde se realizó la venta (hoja Ventas) |
| `orden_id` | NVARCHAR(20) | no | PK | Dimensión degenerada: código de la orden (AR-20001) |
| `cantidad` | INT | no |  | Unidades vendidas (aditiva) |
| `precio_unitario` | DECIMAL(12,2) | no |  | Precio unitario en USD (no aditiva: usar total/cantidad) |
| `total` | DECIMAL(14,2) | no |  | cantidad × precio_unitario en USD (aditiva) |

## Hecho_Finanzas_Mensual

*Tipo:* hecho · *Grano:* Un mes de resultados financieros

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `mes_key` | INT | no | PK FK → Dim_Mes.mes_key | Mes del resultado |
| `ingresos` | DECIMAL(14,2) | no |  | Ingresos del mes, USD |
| `costo_ventas` | DECIMAL(14,2) | no |  | Costo de ventas, USD |
| `gastos_operativos` | DECIMAL(14,2) | no |  | Gastos operativos, USD |
| `utilidad_neta` | DECIMAL(14,2) | no |  | ingresos − costo_ventas − gastos_operativos, USD |
| `flujo_caja` | DECIMAL(14,2) | no |  | Flujo de caja del mes, USD |
| `inversiones_realizadas` | DECIMAL(14,2) | no |  | Inversiones del mes, USD |
| `retorno_inversion` | DECIMAL(12,6) | no |  | utilidad_neta ÷ inversiones_realizadas, como razón (0.94); no aditiva |

## Hecho_Trafico_Web

*Tipo:* hecho · *Grano:* Un cliente por año

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `cliente_key` | INT | no | PK FK → Dim_Cliente.cliente_key | Cliente |
| `region_cliente_key` | INT | no | FK → Dim_Region.region_key | Región del cliente |
| `anio` | SMALLINT | no | PK | Dimensión degenerada: año de los totales |
| `visitas_web` | INT | no |  | Visitas web del año |
| `conversiones_web` | INT | no |  | Conversiones web del año |

## Etl_Rechazos

*Tipo:* control · *Grano:* Una fila de origen que no se cargó

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `rechazo_id` | INT | no | PK | Consecutivo |
| `hoja` | NVARCHAR(50) | no |  | Hoja de origen |
| `fila_excel` | INT | no |  | Número de fila en el Excel (1 = encabezado) |
| `llave_origen` | NVARCHAR(50) | sí |  | OrdenID, ClienteID o Mes de la fila |
| `causa` | NVARCHAR(300) | no |  | Motivo del rechazo |

## Etl_Observaciones

*Tipo:* control · *Grano:* Un dato cargado que requiere revisión

| Columna | Tipo | Nulo | Llave | Descripción |
|---|---|---|---|---|
| `observacion_id` | INT | no | PK | Consecutivo |
| `hoja` | NVARCHAR(50) | no |  | Hoja de origen |
| `fila_excel` | INT | no |  | Número de fila en el Excel (1 = encabezado) |
| `llave_origen` | NVARCHAR(50) | sí |  | OrdenID, ClienteID o Mes de la fila |
| `tipo` | NVARCHAR(50) | no |  | Categoría de la observación |
| `detalle` | NVARCHAR(300) | no |  | Descripción |
