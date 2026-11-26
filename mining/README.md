# Parte 3: minería de datos (K-means)

**Qué es esta carpeta:** el análisis de K-means que agrupa a los 120 clientes según cómo compran. Es la técnica que eligió la Fase 1.

**Para quién:** la persona de la parte 3.

## Qué ya está hecho

- `01_kmeans_clientes.ipynb` corre de principio a fin, sin SQL Server (lee `data/sample/`). Sigue las fases del proceso KDD (Clase 13):
  1. Arma las 7 variables por cliente que define la Fase 1: venta total, órdenes, ticket promedio, % e-commerce, categorías compradas, visitas web y tasa de conversión.
  2. Las estandariza.
  3. Prueba k = 3 a 6 con el método del codo y la silueta.
  4. Arma los grupos y describe el perfil de cada uno.
  5. Exporta el resultado.
- Ya hay una corrida **provisional** (k = 3, nombres genéricos) cuyo resultado ya llega a la base. Así la parte 4 puede usar el filtro "grupo K-means" desde ya.

## Tus pasos

1. Abre el notebook en VS Code o Jupyter con el entorno `.venv` y ejecútalo completo (*Run All*).
2. Revisa las **3 celdas marcadas 🟨 DECISIÓN DEL EQUIPO**:
   - **Variables:** por defecto las 7 de la Fase 1. Si quitas alguna, justifícalo con la tabla de correlación.
   - **k:** por defecto el de mejor silueta (hoy k = 3). Cámbialo en `K_ELEGIDO` si el codo o la interpretación sugieren otro.
   - **Nombres:** escribe una frase por grupo en `NOMBRES`, mirando la tabla de perfil y el mapa de calor. Por ejemplo: "Compra poco, casi siempre en línea".
3. Vuelve a ejecutar el notebook completo y luego carga el resultado en la base:
   ```powershell
   .venv\Scripts\python -m etl.run_etl
   ```
   Con eso `segmento_cluster` queda en `Dim_Cliente` (base y CSV), y el cubo y Power BI lo pueden usar como filtro.
4. **Para el informe (sección 4):** las figuras de `output/figuras/` (elección de k y perfil de grupos), la tabla de perfil y la interpretación de cada grupo.

**Ojo:** la silueta es baja (0.19 con k = 3, la mejor del rango). Los grupos se separan poco: dilo en el informe e interprétalos con cuidado. Si no se pueden describir, el plan B de la Fase 1 es usar los 3 segmentos del Excel (Consumidor, Pyme, Corporativo).

## Archivos

| Archivo | Qué es | ¿Lo editas? |
|---|---|---|
| `01_kmeans_clientes.ipynb` | El análisis completo | Sí, las celdas 🟨 |
| `datos.py` | Carga las tablas desde los CSV (`cargar()`) o desde SQL Server (`cargar("bd")`) | No |
| `output/segmentos_cliente.csv` | Grupo de cada cliente. **Lo lee el ETL** para llenar `Dim_Cliente` | No (lo genera el notebook) |
| `output/perfil_segmentos.csv` | Promedio de cada variable por grupo, con su nombre | No (lo genera el notebook) |
| `output/evaluacion_k.csv`, `output/figuras/` | Codo, silueta y mapa de perfiles | No (lo genera el notebook) |

## Por qué no hay reglas de asociación ni árbol de decisión

La Fase 1 los evaluó y los descartó, y los datos lo confirman: cada orden tiene **un solo producto**, así que no hay canastas para las reglas, y no hay una variable que predecir para el árbol. Ver [`docs/decisiones.md`](../docs/decisiones.md), D7.

## Cómo sabes que terminaste

Los grupos tienen nombre, el ETL dio `OK` después de tu corrida y `Dim_Cliente.segmento_cluster` tiene tus grupos.
