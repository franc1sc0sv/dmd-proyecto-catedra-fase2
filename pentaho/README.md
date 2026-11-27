# Parte 1: ETL en Pentaho Data Integration

**Qué es esta carpeta:** el ETL que propusimos en la Fase 1 (sección 5.2, Tablas 9 y 10), hecho en **Pentaho Data Integration 9.4**. Lee el Excel del caso, lo limpia y carga el Datawarehouse `AndinaRetailDW` en SQL Server. Al final valida la carga contra el Excel y detiene el job si algo no cuadra.

**Para quién:** la parte 1 (ETL). Las demás partes no necesitan Pentaho: trabajan con la base ya cargada o con los CSV de `data/sample/`.

## Qué produce

Las mismas 12 tablas de [`sql/ddl/01_tablas.sql`](../sql/ddl/01_tablas.sql), con **las mismas llaves** que el ETL de Python (`tiempo_key` = AAAAMMDD, `mes_key` = AAAAMM, las demás 1..n en orden alfabético; decisión D1). Por eso los CSV, K-means y Power BI siguen funcionando sin cambios.

## Archivos

| Archivo | Qué hace | Pasos de Pentaho (Fase 1, Tabla 10) |
|---|---|---|
| `andina_etl.kjb` | **Job principal.** Ejecuta todo en orden; si una entrada falla, se detiene | START → SQL → 8 transformaciones → Success / Abort |
| `sql/00_recrear_tablas.sql` | Limpieza: borra y recrea las tablas (carga total) | Paso SQL del job |
| `t01_dim_tiempo.ktr` | 366 días de 2024 | Generate rows, Add sequence, Calculator, Value mapper |
| `t02_dim_mes.ktr` | 12 meses (dimensión conformada) | Generate rows, Add sequence, Value mapper, Add constants |
| `t03_dim_cliente.ktr` | Clientes + `segmento_cluster` de K-means | Excel input, Select values, Unique rows (HashSet), Sort rows, Add sequence, CSV input, Stream lookup |
| `t04_dims_ventas.ktr` | Producto, canal, vendedor y región | Unique rows (HashSet), Append streams, Sort rows, Add sequence |
| `t05_hecho_ventas.ktr` | 850 órdenes | Stream lookup, Calculator, copia en dos ramas, 8 Database lookup, Filter rows |
| `t06_hecho_finanzas.ktr` | 12 meses de finanzas | Value mapper, Filter rows, Calculator, Database lookup |
| `t07_hecho_trafico_web.ktr` | Visitas y conversiones por cliente | Add constants, Select values, Database lookup |
| `t08_validacion.ktr` | Compara Excel ↔ Datawarehouse; aborta si no coincide | Group by, Table input, Join rows, Filter rows, Write to log, Abort |
| `ejecutar_etl.bat` | Corre el job completo con Kitchen y guarda el registro en `logs/etl.log` | — |

Las filas que no se pueden cargar van a `Etl_Rechazos` con su causa (manejo de errores de los pasos); los datos dudosos se cargan y se anotan en `Etl_Observaciones`.

## Instalación (una vez por computadora, Windows)

1. **Java 8 u 11** (por ejemplo Eclipse Temurin 8). Comprobar con `java -version`.
2. **Pentaho Data Integration 9.4 CE** (`pdi-ce-9.4.0.0-343.zip`): descomprimir en `C:\pentaho` para que quede `C:\pentaho\data-integration\Spoon.bat`.
3. **Driver de SQL Server** (no viene con Pentaho): copiar `mssql-jdbc-12.8.1.jre8.jar` a `C:\pentaho\data-integration\lib\`.
4. **Autenticación de Windows:** copiar `mssql-jdbc_auth-12.8.1.x64.dll` a `C:\pentaho\data-integration\libswt\win64\`. Los dos archivos están en Maven Central (`com.microsoft.sqlserver:mssql-jdbc:12.8.1.jre8` y `mssql-jdbc_auth:12.8.1.x64`).
5. **SQL Server con TCP/IP activo en el puerto 1433** (SQL Server Configuration Manager → Protocolos → TCP/IP → Habilitado) y la base creada:
   ```sql
   CREATE DATABASE AndinaRetailDW;
   ```

Si tu servidor no es `localhost:1433`, cambia los parámetros `DW_HOST`, `DW_PORT` y `DW_DB` del job (en Spoon: clic derecho en el lienzo → *Parameters*), o pásalos a Kitchen: `ejecutar_etl.bat /param:DW_HOST=MIPC\SQLEXPRESS`. Si usas usuario y contraseña de SQL Server en vez de Windows, edita la conexión `AndinaRetailDW` y desmarca *Use Integrated Security*.

## Ejecutar

**Con un comando** (desde la raíz del repo):

```powershell
pentaho\ejecutar_etl.bat
```

Debe terminar con `Kitchen termino con codigo 0`. El detalle queda en `pentaho/logs/etl.log`, con la tabla de validación (`xl_` = Excel, `dw_` = Datawarehouse).

**En Spoon** (para las capturas del informe y el video): `C:\pentaho\data-integration\Spoon.bat` → *File → Open* → `pentaho/andina_etl.kjb` → ▶ *Run*. Cada transformación se abre con doble clic sobre su entrada, y se ve el número de filas por paso en *Step Metrics*.

**Segunda comprobación, independiente de Pentaho** (opcional): el validador de Python compara la base con el Excel, los CSV y los KPIs, y regenera `data/sample/reporte_carga.md`:

```powershell
.venv\Scripts\python -m etl.run_etl --validar-bd
```

## Cómo sabes que terminó bien

- El job termina en **Carga completa** (verde) y el paso *Resultado de la validación* muestra: 850 órdenes por $705,113.80, 12 meses con ingresos por $2,331,474.57, 120 clientes con 25,374 visitas y 2,285 conversiones; 366 días, 12 meses, 20 productos, 2 canales, 5 equipos y 4 regiones.
- `Etl_Rechazos` = 0 filas y `Etl_Observaciones` = 3 (las órdenes AR-20354, AR-20550 y AR-20563, anteriores al registro de su cliente).
- `python -m etl.run_etl --validar-bd` dice `OK`.

## Capturas para el informe (sección 2)

1. El job abierto en Spoon después de ejecutarlo (todas las entradas en verde).
2. `t05_hecho_ventas.ktr` con *Step Metrics* (filas leídas, escritas y rechazadas por paso).
3. El registro de *Resultado de la validación* (pestaña *Logging*).
4. En SSMS: conteo de filas por tabla y `SELECT * FROM dbo.Etl_Observaciones`.
