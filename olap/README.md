# Parte 2 (cubo): cubo OLAP en SSAS

**Qué es esta carpeta:** la guía y los cálculos para construir el **cubo SSAS multidimensional** que prometió la Fase 1.

**Para quién:** la persona de la parte 2.

## Qué ya está hecho y qué falta

| Pieza | Estado |
|---|---|
| Cubo hecho en SQL (`dbo.vw_Cubo_Ventas`, con `ROLLUP` y `CUBE`) | ✅ Funciona; sirve de respaldo y de evidencia |
| Fórmulas de los KPIs para el cubo (`ssas/kpis_calculados.mdx`) | Esqueleto listo para pegar |
| **Proyecto SSAS** (Visual Studio) | ⬜ **Por construir**: es tu tarea principal |

## Tus pasos

Requisitos: el servicio *SQL Server Analysis Services* en modo **Multidimensional** y Visual Studio con la extensión *Analysis Services Projects*.

1. Asegúrate de que la base esté cargada (`.venv\Scripts\python -m etl.run_etl` da `OK`).
2. En Visual Studio: nuevo proyecto **Analysis Services Multidimensional** guardado en `olap/ssas/AndinaRetail_Cubo/`.
3. **Data Source:** SQL Server `localhost`, base `AndinaRetailDW`, cuenta de servicio.
4. **Data Source View:** agrega las 10 tablas (no las `Etl_*`). Las relaciones salen solas de las llaves de la base. Verifica que `Dim_Region` esté unida **dos veces** a `Hecho_Ventas` y que `Dim_Mes` esté unida a **los dos hechos** (`mes_key`).
5. **Dimensiones** (con sus jerarquías):
   - *Tiempo* (Dim_Tiempo): `anio → semestre → trimestre → nombre_mes → fecha`. Ordena `nombre_mes` por `mes_numero`.
   - *Mes* (Dim_Mes): `anio → trimestre → nombre_mes`.
   - *Cliente*: atributos `segmento`, `segmento_cluster` (grupo de K-means) y `cliente_id`.
   - *Producto*: `categoria → producto`.
   - *Canal*, *Vendedor* y *Region*: simples.
6. **Cubo** con tres grupos de medidas:
   - Hecho_Ventas: `total`, `cantidad` y el conteo de filas (= órdenes). En un grupo aparte, *Distinct Count* de `cliente_key`.
   - Hecho_Finanzas_Mensual: sumas.
   - Hecho_Trafico_Web: sumas.
7. **Uso de dimensiones:** agrega *Region* dos veces, como "Región Venta" (`region_venta_key`) y "Región Cliente" (`region_cliente_key`). *Mes* se relaciona con Ventas y con Finanzas por `mes_key`. Eso permite comparar ambos hechos (el «cubo virtual» de la Clase 10).
8. **Cálculos:** pega `ssas/kpis_calculados.mdx` en la pestaña *Calculations* (vista de script). Ajusta los nombres de las medidas si en tu proyecto quedaron distintos.
9. **Desplegar y procesar.** Con SQL Server 2025 *Standard Developer*, el botón Deploy de Visual Studio puede fallar con *"The current edition 'StandardDeveloper64' … is not supported by the client"*. Si pasa, despliega el `.asdatabase` compilado con el proveedor MSOLAP desde PowerShell. Leandro tiene un script que ya resolvió esto en un proyecto anterior.
10. **Verificar:** en SSMS (conexión a Analysis Services), los KPIs anuales del cubo deben dar lo mismo que `SELECT * FROM dbo.vw_KPI_Anual`.

## Si el cubo SSAS no sale a tiempo

Usa `dbo.vw_Cubo_Ventas` y `sql/olap/02_operadores_olap.sql` como evidencia de análisis multidimensional (es un cubo ROLAP en vez de MOLAP; Clase 10) y anótalo en `docs/decisiones.md`, D6.

Ejemplo sobre la vista:

```sql
-- Ventas por categoría y canal (el resto de dimensiones en "Todos")
SELECT categoria, canal, ventas, ordenes, ticket_promedio
FROM dbo.vw_Cubo_Ventas
WHERE anio IS NULL   -- total general del ROLLUP (con un solo año, es igual al total de 2024)
  AND nivel_todas_categorias = 0 AND nivel_todos_canales = 0
  AND nivel_todas_regiones = 1 AND nivel_todos_segmentos = 1 AND nivel_todos_clusters = 1
ORDER BY categoria, canal;
```

## Cómo sabes que terminaste

El cubo está procesado, se puede navegar por año → trimestre → mes y por categoría → producto, y sus KPIs coinciden con `vw_KPI_Anual`.
