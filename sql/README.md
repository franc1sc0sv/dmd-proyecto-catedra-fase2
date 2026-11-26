# SQL (SQL Server, base `AndinaRetailDW`)

| Carpeta | Contenido | ¿Lo ejecuta el ETL? |
|---|---|---|
| `ddl/01_tablas.sql` | Las 12 tablas (10 del modelo + 2 de control). **Generado** desde `etl/contrato.py` | Sí, en cada carga |
| `kpis/01_vistas_kpi.sql` | `vw_KPI_Anual`, `vw_KPI_Finanzas_Mensual`, `vw_KPI_Ventas_Mensual` | Sí |
| `kpis/02_consultas_kpi.sql` | Consultas de evidencia para capturas del informe | No: correr en SSMS |
| `olap/01_vistas_cubo.sql` | `vw_Cubo_Ventas` con `ROLLUP` + `CUBE` | Sí |

Conexión en SSMS: servidor `localhost`, autenticación de Windows, marcar *Trust server certificate*.

Convención: los archivos que crean vistas llevan `vistas` en el nombre y usan `CREATE OR ALTER VIEW`; el ETL los ejecuta en orden.
