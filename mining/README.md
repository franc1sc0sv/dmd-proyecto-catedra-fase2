# Parte 3: minería de datos

La Fase 1 seleccionó **K-means** para segmentar a los 120 clientes. Las reglas de asociación y el árbol de decisión se descartaron allí: cada orden tiene un solo producto, así que no hay canastas, y no hay variable objetivo. Los datos lo confirman (`docs/decisiones.md`, D7).

## `01_kmeans_clientes.ipynb`

Corre de punta a punta contra `data/sample/` con semilla fija (42):

1. Las 7 variables por cliente de la Fase 1 (venta total, órdenes, ticket, % e-commerce, categorías, visitas web, tasa de conversión).
2. Estandarización.
3. k de 3 a 6: método del codo y silueta.
4. Modelo final; grupos renumerados 1..k por venta promedio.
5. Perfil de cada grupo y cruce con el `segmento` del Excel.
6. Exporta `output/segmentos_cliente.csv`, `perfil_segmentos.csv`, `evaluacion_k.csv` y figuras.

**🟨 Decisiones del equipo** (celdas marcadas en el notebook): variables, k y nombre/interpretación de cada grupo.

**Ojo:** con estos datos la silueta es baja (0.19 con k = 3, la mejor del rango). Los grupos se separan poco: hay que interpretarlos con cuidado y decirlo en el informe. Si no se pueden describir, el plan B de la Fase 1 es usar los 3 segmentos del Excel.

## Llevar el segmento al DW

```
python -m jupyter nbconvert --to notebook --execute --inplace mining/01_kmeans_clientes.ipynb
python -m etl.run_etl
```

El ETL integra `output/segmentos_cliente.csv` en `Dim_Cliente.segmento_cluster` (BD y muestra). Lo que está hoy en `output/` es la corrida por defecto (k = 3, nombres genéricos): **es provisional** hasta que el equipo tome sus decisiones.

Para leer de la BD en vez de la muestra: `cargar("bd")` o la variable de entorno `FUENTE=bd`.
