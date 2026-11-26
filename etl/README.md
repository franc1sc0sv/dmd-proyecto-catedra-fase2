# Parte 1: ETL

```
python -m etl.run_etl            # completo (SQL Server)
python -m etl.run_etl --sin-bd   # solo data/sample
python -m etl.generar            # tras cambiar contrato.py: DDL, diccionario, Power Query
```

| Archivo | Qué hace |
|---|---|
| `contrato.py` | **Esquema estrella**: tablas, columnas, tipos, llaves. Fuente única de verdad |
| `extract.py` | Lee las 3 hojas sin inferir tipos |
| `transform.py` | Reglas de limpieza (`docs/reglas_limpieza.md`), dimensiones, hechos, rechazos y observaciones |
| `load.py` | Escribe `data/sample/`; crea la BD si falta, recrea las tablas (carga total), inserta y crea las vistas |
| `validate.py` | Conciliación Excel ↔ transformación ↔ muestra ↔ BD, esquema BD = contrato, KPIs SQL = Excel |
| `generar.py` | Genera `sql/ddl/01_tablas.sql`, `docs/diccionario_datos.md` y `powerbi/power_query/*.pq` |

Si `mining/output/segmentos_cliente.csv` existe, el ETL lo usa para llenar `Dim_Cliente.segmento_cluster`.

**Pendiente:** decidir si se mantiene Python o se replica en Pentaho (`docs/decisiones.md`, D4). Si se usa Pentaho, debe escribir en las tablas de `sql/ddl/01_tablas.sql`; la validación se puede seguir corriendo con este módulo como control.
