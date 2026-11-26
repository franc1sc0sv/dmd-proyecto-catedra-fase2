# Definición de KPIs

Los 10 KPIs de la Fase 1 (sección 3). "Valor 2024" es el resultado sin filtros; el ETL lo verifica en cada carga contra un cálculo hecho directamente sobre el Excel (`data/sample/reporte_carga.md`).

Dónde está implementado cada uno: SQL en `sql/kpis/01_vistas_kpi.sql` (`vw_KPI_Anual`, `vw_KPI_Finanzas_Mensual`, `vw_KPI_Ventas_Mensual`), DAX en `powerbi/medidas.dax`, MDX en `olap/ssas/kpis_calculados.mdx`.

**Regla común:** los porcentajes se recalculan a partir de sumas en cada nivel (nunca se promedian porcentajes ni `retorno_inversion`).

## Finanzas (fuente: Hecho_Finanzas_Mensual · grano: mes · se analiza por mes y año vía Dim_Mes)

| KPI | Fórmula | Unidad | Valor 2024 | Notas |
|---|---|---|---|---|
| Margen bruto | (Σingresos − Σcosto_ventas) ÷ Σingresos × 100 | % | **41.57** | Alerta si < 40 %: marzo (39.08), abril (39.50), mayo (38.54) |
| Margen neto | Σutilidad_neta ÷ Σingresos × 100 | % | **26.90** | |
| Índice de gastos operativos | Σgastos_operativos ÷ Σingresos × 100 | % | **14.66** | |
| ROI | Σutilidad_neta ÷ Σinversiones_realizadas × 100 | % | **106.71** | Utilidad del período sobre lo invertido en el mismo período |
| Flujo de caja acumulado | Σflujo_caja desde enero hasta el mes | USD | **450,917.68** | Acumulado dentro del año |

## Ventas (fuente: Hecho_Ventas · grano: orden · filtrable por mes, categoría, producto, canal, vendedor, región de venta/cliente, segmento y grupo K-means)

| KPI | Fórmula | Unidad | Valor 2024 | Notas |
|---|---|---|---|---|
| Crecimiento de ventas | (ventas mes − ventas mes anterior) ÷ ventas mes anterior × 100 | % | −22.84 (mayo) a +49.08 (octubre) | Mensual. **Diciembre es parcial** (ventas hasta el día 20): su −56.13 % no es comparable; reportar hasta noviembre |
| Ventas por cliente | Σtotal ÷ clientes distintos con compra | USD | **5,875.95** | 705,113.80 ÷ 120 |
| Ticket promedio | Σtotal ÷ órdenes | USD | **829.55** | 705,113.80 ÷ 850 |
| Participación del e-commerce | Σtotal canal E-commerce ÷ Σtotal × 100 | % | **44.00** | Tienda física 56.00 % |

## Tráfico web (fuente: Hecho_Trafico_Web · grano: cliente-año)

| KPI | Fórmula | Unidad | Valor 2024 | Notas |
|---|---|---|---|---|
| Tasa de conversión web | Σconversiones_web ÷ Σvisitas_web × 100 | % | **9.01** | 2,285 ÷ 25,374. Solo anual: no se reparte por mes. Filtrable por cliente, segmento y región del cliente |

## Comprobación a mano (para el informe)

En el Excel original, hoja Finanzas_Mensual: `=(SUMA(B2:B13)-SUMA(C2:C13))/SUMA(B2:B13)` → 0.4157 = **41.57 %**, igual a `SELECT margen_bruto_pct FROM dbo.vw_KPI_Anual`. Hoja Ventas: `=SUMA(I2:I851)/850` → **829.55** = `ticket_promedio`.

## Metas

La Fase 1 dejó las metas "para acordar con las áreas en la Fase 2"; solo fijó el umbral de alerta de 40 % para el margen bruto. **Pendiente de decidir por el equipo.**
