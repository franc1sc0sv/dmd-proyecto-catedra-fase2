-- Vistas de los 10 KPIs de la Fase 1 (secciones 3.1 y 3.2).
-- Las crea el ETL en cada carga. Definiciones: docs/kpis.md
-- Porcentajes en escala 0-100. Montos en USD.

-- ------------------------------------------------------------ Finanzas, por mes
CREATE OR ALTER VIEW dbo.vw_KPI_Finanzas_Mensual AS
SELECT
    m.mes_key, m.anio, m.mes_numero, m.nombre_mes, m.trimestre,
    f.ingresos, f.costo_ventas, f.gastos_operativos, f.utilidad_neta, f.flujo_caja, f.inversiones_realizadas,
    CAST(100.0 * (f.ingresos - f.costo_ventas) / NULLIF(f.ingresos, 0) AS DECIMAL(9,2))  AS margen_bruto_pct,
    CAST(100.0 * f.utilidad_neta / NULLIF(f.ingresos, 0) AS DECIMAL(9,2))                AS margen_neto_pct,
    CAST(100.0 * f.gastos_operativos / NULLIF(f.ingresos, 0) AS DECIMAL(9,2))            AS indice_gastos_operativos_pct,
    CAST(100.0 * f.utilidad_neta / NULLIF(f.inversiones_realizadas, 0) AS DECIMAL(9,2))  AS roi_pct,
    SUM(f.flujo_caja) OVER (PARTITION BY m.anio ORDER BY m.mes_numero
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)            AS flujo_caja_acumulado,
    CASE WHEN 100.0 * (f.ingresos - f.costo_ventas) / NULLIF(f.ingresos, 0) < 40
         THEN 1 ELSE 0 END                                                               AS alerta_margen_bruto
FROM dbo.Hecho_Finanzas_Mensual f
JOIN dbo.Dim_Mes m ON m.mes_key = f.mes_key;
GO

-- ------------------------------------------------------------ Ventas, por mes
CREATE OR ALTER VIEW dbo.vw_KPI_Ventas_Mensual AS
WITH base AS (
    SELECT t.anio, t.mes_key, t.mes_numero, t.nombre_mes,
           SUM(v.total) AS ventas,
           COUNT(DISTINCT v.orden_id) AS ordenes,
           COUNT(DISTINCT v.cliente_key) AS clientes,
           SUM(CASE WHEN c.canal = N'E-commerce' THEN v.total ELSE 0 END) AS ventas_ecommerce,
           MAX(t.fecha) AS ultima_fecha
    FROM dbo.Hecho_Ventas v
    JOIN dbo.Dim_Tiempo t ON t.tiempo_key = v.tiempo_key
    JOIN dbo.Dim_Canal  c ON c.canal_key  = v.canal_key
    GROUP BY t.anio, t.mes_key, t.mes_numero, t.nombre_mes
)
SELECT
    anio, mes_key, mes_numero, nombre_mes, ventas, ordenes, clientes,
    CAST(ventas / NULLIF(ordenes, 0) AS DECIMAL(14,2))                   AS ticket_promedio,
    CAST(ventas / NULLIF(clientes, 0) AS DECIMAL(14,2))                  AS ventas_por_cliente,
    CAST(100.0 * ventas_ecommerce / NULLIF(ventas, 0) AS DECIMAL(9,2))   AS participacion_ecommerce_pct,
    LAG(ventas) OVER (PARTITION BY anio ORDER BY mes_numero)            AS ventas_mes_anterior,
    CAST(100.0 * (ventas - LAG(ventas) OVER (PARTITION BY anio ORDER BY mes_numero))
         / NULLIF(LAG(ventas) OVER (PARTITION BY anio ORDER BY mes_numero), 0) AS DECIMAL(9,2)) AS crecimiento_ventas_pct,
    -- El último mes con datos es parcial si la última venta no cae en fin de mes
    -- (diciembre 2024 llega al día 20: su crecimiento no es comparable, Fase 1, 3.2).
    CASE WHEN ultima_fecha = MAX(ultima_fecha) OVER ()
          AND ultima_fecha < EOMONTH(ultima_fecha) THEN 1 ELSE 0 END    AS mes_parcial
FROM base;
GO

-- ------------------------------------------------------------ Los 10 KPIs, anual
CREATE OR ALTER VIEW dbo.vw_KPI_Anual AS
WITH fin AS (
    SELECT m.anio, SUM(f.ingresos) ingresos, SUM(f.costo_ventas) costo_ventas,
           SUM(f.gastos_operativos) gastos_operativos, SUM(f.utilidad_neta) utilidad_neta,
           SUM(f.flujo_caja) flujo_caja, SUM(f.inversiones_realizadas) inversiones
    FROM dbo.Hecho_Finanzas_Mensual f JOIN dbo.Dim_Mes m ON m.mes_key = f.mes_key
    GROUP BY m.anio
), ven AS (
    SELECT t.anio, SUM(v.total) ventas, COUNT(DISTINCT v.orden_id) ordenes,
           COUNT(DISTINCT v.cliente_key) clientes,
           SUM(CASE WHEN c.canal = N'E-commerce' THEN v.total ELSE 0 END) ventas_ecommerce
    FROM dbo.Hecho_Ventas v
    JOIN dbo.Dim_Tiempo t ON t.tiempo_key = v.tiempo_key
    JOIN dbo.Dim_Canal c  ON c.canal_key  = v.canal_key
    GROUP BY t.anio
), web AS (
    SELECT anio, SUM(visitas_web) visitas, SUM(conversiones_web) conversiones
    FROM dbo.Hecho_Trafico_Web GROUP BY anio
)
SELECT
    fin.anio,
    -- Finanzas
    CAST(100.0 * (fin.ingresos - fin.costo_ventas) / NULLIF(fin.ingresos, 0) AS DECIMAL(9,2)) AS margen_bruto_pct,
    CAST(100.0 * fin.utilidad_neta / NULLIF(fin.ingresos, 0) AS DECIMAL(9,2))                AS margen_neto_pct,
    CAST(100.0 * fin.gastos_operativos / NULLIF(fin.ingresos, 0) AS DECIMAL(9,2))            AS indice_gastos_operativos_pct,
    CAST(100.0 * fin.utilidad_neta / NULLIF(fin.inversiones, 0) AS DECIMAL(9,2))             AS roi_pct,
    fin.flujo_caja                                                                           AS flujo_caja_acumulado,
    -- Ventas (el crecimiento es mensual: ver vw_KPI_Ventas_Mensual)
    CAST(ven.ventas / NULLIF(ven.clientes, 0) AS DECIMAL(14,2))                              AS ventas_por_cliente,
    CAST(100.0 * web.conversiones / NULLIF(web.visitas, 0) AS DECIMAL(9,2))                  AS tasa_conversion_web_pct,
    CAST(ven.ventas / NULLIF(ven.ordenes, 0) AS DECIMAL(14,2))                               AS ticket_promedio,
    CAST(100.0 * ven.ventas_ecommerce / NULLIF(ven.ventas, 0) AS DECIMAL(9,2))               AS participacion_ecommerce_pct,
    -- Totales de control
    ven.ventas AS ventas_total, ven.ordenes, ven.clientes, fin.ingresos AS ingresos_total,
    web.visitas, web.conversiones
FROM fin
JOIN ven ON ven.anio = fin.anio
JOIN web ON web.anio = fin.anio;
GO
