# Parte 2: cubo OLAP

La Fase 1 eligió un **cubo SSAS multidimensional** sobre el esquema estrella. Hay dos piezas:

| Pieza | Estado | Para qué |
|---|---|---|
| `sql/olap/01_vistas_cubo.sql` → `dbo.vw_Cubo_Ventas` | ✅ Funciona (la crea el ETL) | Cubo relacional con `ROLLUP` (tiempo) y `CUBE` (categoría, canal, región, segmento, grupo K-means). Respaldo y evidencia si SSAS se complica |
| `ssas/` (proyecto de Visual Studio) | ⬜ Por construir | El cubo de la Fase 1 |
| `ssas/kpis_calculados.mdx` | Esqueleto | Miembros calculados de los KPIs |

## Construir el cubo SSAS

Requisitos: SQL Server Analysis Services en modo **Multidimensional** (servicio `MSSQLServerOLAPService`) y Visual Studio con la extensión *Analysis Services Projects*.

1. Correr el ETL para tener `AndinaRetailDW` cargada.
2. Nuevo proyecto **Analysis Services Multidimensional** en `olap/ssas/AndinaRetail_Cubo/`.
3. **Data Source:** SQL Server `localhost`, base `AndinaRetailDW`, cuenta de servicio.
4. **Data Source View:** las 10 tablas (no las `Etl_*`). Las FK de la BD crean las relaciones; verifica que `Dim_Region` quede ligada dos veces a `Hecho_Ventas` y que `Dim_Mes` quede ligada a los dos hechos (`mes_key`).
5. **Dimensiones:**
   - *Tiempo* (Dim_Tiempo): jerarquía `anio → semestre → trimestre → nombre_mes → fecha` (ordena `nombre_mes` por `mes_numero`).
   - *Mes* (Dim_Mes): `anio → trimestre → nombre_mes`.
   - *Cliente*: atributos `segmento`, `segmento_cluster`, `cliente_id`.
   - *Producto*: `categoria → producto`.
   - *Canal*, *Vendedor*, *Region* (simples).
6. **Cubo** con tres grupos de medidas: Hecho_Ventas (`total`, `cantidad`, conteo de filas = órdenes, y un grupo aparte con *Distinct Count* de `cliente_key`), Hecho_Finanzas_Mensual (sumas), Hecho_Trafico_Web (sumas).
7. **Uso de dimensiones:** *Region* se agrega dos veces como dimensión de cubo: "Región Venta" (`region_venta_key`) y "Región Cliente" (`region_cliente_key`). *Mes* es la dimensión **conformada**: relación regular con Ventas y con Finanzas por `mes_key`, lo que permite cruzar ambos grupos de medidas (el «cubo virtual» de la Clase 10).
8. **Cálculos:** pegar `ssas/kpis_calculados.mdx` en la pestaña Calculations (vista de script) y ajustar los nombres de medidas si difieren.
9. **Desplegar y procesar.** Con SQL Server 2025 Standard Developer, *Deploy* de Visual Studio puede fallar con *"The current edition 'StandardDeveloper64' … is not supported by the client"*. Si pasa, desplegar el `.asdatabase` compilado por el proveedor MSOLAP desde PowerShell (Leandro ya tiene un script que funciona para esto de un proyecto anterior).
10. **Verificar** que en SSMS (conexión a Analysis Services) los KPIs anuales den lo mismo que `SELECT * FROM dbo.vw_KPI_Anual`.

## Consultas de ejemplo sobre la vista CUBE/ROLLUP

```sql
-- Ventas por categoría y canal (todas las demás dimensiones en "Todos")
SELECT categoria, canal, ventas, ordenes, ticket_promedio
FROM dbo.vw_Cubo_Ventas
WHERE anio IS NULL                       -- total del año (nivel superior del ROLLUP)
  AND nivel_todas_categorias = 0 AND nivel_todos_canales = 0
  AND nivel_todas_regiones = 1 AND nivel_todos_segmentos = 1 AND nivel_todos_clusters = 1
ORDER BY categoria, canal;
```
