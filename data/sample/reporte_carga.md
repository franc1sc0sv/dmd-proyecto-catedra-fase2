# Reporte de carga

Generado: 2026-11-26 01:43 · Excel SHA256 `7e9568e27043…` · BD: sí · **Resultado: OK**

## Conciliación

| Verificación | OK | Detalle |
|---|---|---|
| Ventas: leídas = cargadas + rechazadas + no-registro | ✅ | 850 = 850 + 0 + 0 |
| Clientes: leídas = cargadas + rechazadas + no-registro | ✅ | 120 = 120 + 0 + 0 |
| Finanzas_Mensual: leídas = cargadas + rechazadas + no-registro | ✅ | 15 = 12 + 0 + 3 |
| Total ventas | ✅ | Excel 705,113.80 · transformación 705,113.80 · muestra 705,113.80 · BD 705,113.80 |
| Total ingresos | ✅ | Excel 2,331,474.57 · transformación 2,331,474.57 · muestra 2,331,474.57 · BD 2,331,474.57 |
| Total visitas_web | ✅ | Excel 25,374 · transformación 25,374 · muestra 25,374 · BD 25,374 |
| Total conversiones_web | ✅ | Excel 2,285 · transformación 2,285 · muestra 2,285 · BD 2,285 |
| Filas Dim_Mes | ✅ | transf. 12 · muestra 12 · BD 12 · distintos Excel 12 |
| Filas Dim_Tiempo | ✅ | transf. 366 · muestra 366 · BD 366 |
| Filas Dim_Cliente | ✅ | transf. 120 · muestra 120 · BD 120 · distintos Excel 120 |
| Filas Dim_Producto | ✅ | transf. 20 · muestra 20 · BD 20 · distintos Excel 20 |
| Filas Dim_Canal | ✅ | transf. 2 · muestra 2 · BD 2 · distintos Excel 2 |
| Filas Dim_Vendedor | ✅ | transf. 5 · muestra 5 · BD 5 · distintos Excel 5 |
| Filas Dim_Region | ✅ | transf. 4 · muestra 4 · BD 4 · distintos Excel 4 |
| Filas Hecho_Ventas | ✅ | transf. 850 · muestra 850 · BD 850 |
| Filas Hecho_Finanzas_Mensual | ✅ | transf. 12 · muestra 12 · BD 12 |
| Filas Hecho_Trafico_Web | ✅ | transf. 120 · muestra 120 · BD 120 |
| Filas Etl_Rechazos | ✅ | transf. 0 · muestra 0 · BD 0 |
| Filas Etl_Observaciones | ✅ | transf. 3 · muestra 3 · BD 3 |
| Esquema Dim_Mes = contrato | ✅ |  |
| Esquema Dim_Tiempo = contrato | ✅ |  |
| Esquema Dim_Cliente = contrato | ✅ |  |
| Esquema Dim_Producto = contrato | ✅ |  |
| Esquema Dim_Canal = contrato | ✅ |  |
| Esquema Dim_Vendedor = contrato | ✅ |  |
| Esquema Dim_Region = contrato | ✅ |  |
| Esquema Hecho_Ventas = contrato | ✅ |  |
| Esquema Hecho_Finanzas_Mensual = contrato | ✅ |  |
| Esquema Hecho_Trafico_Web = contrato | ✅ |  |
| Esquema Etl_Rechazos = contrato | ✅ |  |
| Esquema Etl_Observaciones = contrato | ✅ |  |
| KPI margen_bruto_pct | ✅ | SQL 41.57 · Excel 41.57 |
| KPI margen_neto_pct | ✅ | SQL 26.90 · Excel 26.90 |
| KPI indice_gastos_operativos_pct | ✅ | SQL 14.66 · Excel 14.66 |
| KPI roi_pct | ✅ | SQL 106.71 · Excel 106.71 |
| KPI flujo_caja_acumulado | ✅ | SQL 450,917.68 · Excel 450,917.68 |
| KPI ventas_por_cliente | ✅ | SQL 5,875.95 · Excel 5,875.95 |
| KPI tasa_conversion_web_pct | ✅ | SQL 9.01 · Excel 9.01 |
| KPI ticket_promedio | ✅ | SQL 829.55 · Excel 829.55 |
| KPI participacion_ecommerce_pct | ✅ | SQL 44.00 · Excel 44.00 |

## Filas que no se cargaron

**Rechazos: 0.** Ninguna fila de datos se descartó.

Filas que no son registros (no se cuentan como rechazos, Fase 1 tabla 1):

| Hoja | Fila Excel | Contenido |
|---|---|---|
| Finanzas_Mensual | 14 | (vacía) |
| Finanzas_Mensual | 15 | (vacía) |
| Finanzas_Mensual | 16 | Nota: cifras en USD. Datos simulados con fines académicos para el Proyecto de Cátedra DMD 941. |

## Observaciones (se cargan, pero requieren revisión)

- **Orden anterior al registro del cliente**: 3

Detalle completo: `Etl_Observaciones.csv` / tabla `dbo.Etl_Observaciones`.
