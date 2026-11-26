-- Consultas de evidencia de los KPIs (para capturas del informe, sección 3).
-- Ejecutar en SSMS sobre AndinaRetailDW. No las ejecuta el ETL.

-- Los 10 KPIs del año
SELECT * FROM dbo.vw_KPI_Anual;

-- Finanzas mes a mes (margen bruto < 40 % marcado en alerta_margen_bruto)
SELECT nombre_mes, ingresos, margen_bruto_pct, margen_neto_pct, indice_gastos_operativos_pct,
       roi_pct, flujo_caja, flujo_caja_acumulado, alerta_margen_bruto
FROM dbo.vw_KPI_Finanzas_Mensual ORDER BY mes_key;

-- Ventas mes a mes con crecimiento (diciembre es parcial)
SELECT nombre_mes, ventas, ordenes, ticket_promedio, participacion_ecommerce_pct,
       crecimiento_ventas_pct, mes_parcial
FROM dbo.vw_KPI_Ventas_Mensual ORDER BY mes_key;

-- Ticket promedio y participación por canal
SELECT c.canal, SUM(v.total) AS ventas, COUNT(*) AS ordenes,
       CAST(SUM(v.total) / COUNT(*) AS DECIMAL(14,2)) AS ticket_promedio,
       CAST(100.0 * SUM(v.total) / SUM(SUM(v.total)) OVER () AS DECIMAL(5,2)) AS participacion_pct
FROM dbo.Hecho_Ventas v JOIN dbo.Dim_Canal c ON c.canal_key = v.canal_key
GROUP BY c.canal;

-- Tasa de conversión web por segmento del Excel y por grupo K-means
SELECT cl.segmento, cl.segmento_cluster,
       SUM(w.visitas_web) AS visitas, SUM(w.conversiones_web) AS conversiones,
       CAST(100.0 * SUM(w.conversiones_web) / NULLIF(SUM(w.visitas_web), 0) AS DECIMAL(5,2)) AS tasa_conversion_pct
FROM dbo.Hecho_Trafico_Web w JOIN dbo.Dim_Cliente cl ON cl.cliente_key = w.cliente_key
GROUP BY cl.segmento, cl.segmento_cluster ORDER BY cl.segmento, cl.segmento_cluster;

-- Control: filas rechazadas y observaciones del ETL
SELECT * FROM dbo.Etl_Rechazos;
SELECT * FROM dbo.Etl_Observaciones;
