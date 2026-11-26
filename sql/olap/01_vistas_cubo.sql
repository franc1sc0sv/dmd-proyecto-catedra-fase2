-- Cubo relacional de ventas con ROLLUP (jerarquía de tiempo) y CUBE (resto de dimensiones).
-- Es el respaldo del cubo SSAS (olap/) y sirve como evidencia de análisis multidimensional.
-- Columnas en NULL + nivel_* = 1 indican "Todos" en esa dimensión.

CREATE OR ALTER VIEW dbo.vw_Cubo_Ventas AS
SELECT
    t.anio, t.trimestre, t.mes_numero,
    p.categoria, c.canal, r.region AS region_venta, cl.segmento, cl.segmento_cluster,
    SUM(v.total)                                              AS ventas,
    SUM(v.cantidad)                                           AS unidades,
    COUNT(DISTINCT v.orden_id)                                AS ordenes,
    CAST(SUM(v.total) / NULLIF(COUNT(DISTINCT v.orden_id), 0) AS DECIMAL(14,2)) AS ticket_promedio,
    GROUPING(t.trimestre)        AS nivel_todos_trimestres,
    GROUPING(t.mes_numero)       AS nivel_todos_meses,
    GROUPING(p.categoria)        AS nivel_todas_categorias,
    GROUPING(c.canal)            AS nivel_todos_canales,
    GROUPING(r.region)           AS nivel_todas_regiones,
    GROUPING(cl.segmento)        AS nivel_todos_segmentos,
    GROUPING(cl.segmento_cluster) AS nivel_todos_clusters
FROM dbo.Hecho_Ventas v
JOIN dbo.Dim_Tiempo   t  ON t.tiempo_key   = v.tiempo_key
JOIN dbo.Dim_Producto p  ON p.producto_key = v.producto_key
JOIN dbo.Dim_Canal    c  ON c.canal_key    = v.canal_key
JOIN dbo.Dim_Region   r  ON r.region_key   = v.region_venta_key
JOIN dbo.Dim_Cliente  cl ON cl.cliente_key = v.cliente_key
GROUP BY ROLLUP (t.anio, t.trimestre, t.mes_numero),
         CUBE (p.categoria, c.canal, r.region, cl.segmento, cl.segmento_cluster);
GO
