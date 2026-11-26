# Parte 2 (SQL): tablas, KPIs y cubo en SQL

**Qué es esta carpeta:** todo el SQL del proyecto para SQL Server, base `AndinaRetailDW`.

**Para quién:** sobre todo la parte 2 (KPIs). La parte 1 usa `ddl/` y todos pueden usar las consultas de evidencia para sus capturas.

## Qué hay

| Archivo | Qué es | ¿Quién lo ejecuta? |
|---|---|---|
| `ddl/01_tablas.sql` | Crea las 12 tablas (10 del modelo + 2 de control). Se genera desde `etl/contrato.py`: no editarlo a mano | El ETL, en cada carga |
| `kpis/01_vistas_kpi.sql` | Tres vistas con los 10 KPIs: `vw_KPI_Anual`, `vw_KPI_Finanzas_Mensual` y `vw_KPI_Ventas_Mensual` | El ETL, en cada carga |
| `kpis/02_consultas_kpi.sql` | Consultas para mostrar los KPIs (capturas del informe, sección 3) | Tú, en SSMS |
| `olap/01_vistas_cubo.sql` | `vw_Cubo_Ventas`: un cubo hecho en SQL con `ROLLUP` y `CUBE` | El ETL, en cada carga |
| `olap/02_operadores_olap.sql` | Un ejemplo de cada operador OLAP: drill, roll, slice, dice y pivot (Clase 15.4) | Tú, en SSMS |

## Tus pasos (parte 2)

1. Abre **SSMS** → servidor `localhost`, autenticación de Windows, marca *Trust server certificate* → base `AndinaRetailDW`.
2. Ejecuta `kpis/02_consultas_kpi.sql`. La primera consulta (`SELECT * FROM dbo.vw_KPI_Anual`) debe dar los valores de [`docs/kpis.md`](../docs/kpis.md): margen bruto 41.57, ticket 829.55, etc.
3. Toma las capturas para la sección 3 del informe. Para la comprobación manual, `docs/kpis.md` trae dos fórmulas de Excel que dan el mismo resultado que SQL.
4. Ejecuta `olap/02_operadores_olap.sql` y toma capturas de cada operador para la sección 4.
5. Sigue con el cubo SSAS: [`olap/README.md`](../olap/README.md).

## Cómo sabes que terminaste

Tienes capturas de los 10 KPIs con valores reales y de los 5 operadores OLAP, y los valores coinciden con `docs/kpis.md`.
