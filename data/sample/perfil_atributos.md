# Informe de estado de los atributos

Perfilado del Excel **antes** de limpiar (Clase 15.3). Los mínimos y máximos de atributos nominales son alfabéticos, como en SQL. `Fecha` y `FechaRegistro` aparecen como *Nominal* porque vienen como texto (regla F2 de `docs/reglas_limpieza.md`). Las 3 filas sin datos de Finanzas_Mensual (2 vacías + nota) explican sus nulos.

## Ventas

| Atributo | Tipo | #total | #nulos | #distintos | Media | Desv. | Moda | Mín. | Máx. |
|---|---|---|---|---|---|---|---|---|---|
| OrdenID | Nominal | 850 | 0 | 850 |  |  | AR-20001 | AR-20001 | AR-20850 |
| Fecha | Nominal | 850 | 0 | 325 |  |  | 2024-02-16 | 2024-01-01 | 2024-12-20 |
| ClienteID | Nominal | 850 | 0 | 120 |  |  | CLI-0077 | CLI-0001 | CLI-0120 |
| Categoria | Nominal | 850 | 0 | 4 |  |  | Cómputo | Cómputo | Línea Blanca |
| Producto | Nominal | 850 | 0 | 20 |  |  | Audífonos Bluetooth | Aire acondicionado | Tablet 10" |
| Canal | Nominal | 850 | 0 | 2 |  |  | Tienda física | E-commerce | Tienda física |
| Cantidad | Numérico | 850 | 0 | 5 | 2.92 | 1.40 | 3 | 1 | 5 |
| PrecioUnitario | Numérico | 850 | 0 | 832 | 282.53 | 206.92 | 34.65 | 33.44 | 701.03 |
| Total | Numérico | 850 | 0 | 844 | 829.55 | 788.14 | 72.18 | 33.99 | 3,505.15 |
| Vendedor | Nominal | 850 | 0 | 5 |  |  | Equipo Zacatecoluca | Equipo E-commerce | Equipo Zacatecoluca |
| Region | Nominal | 850 | 0 | 4 |  |  | Región Occidental | Región Central | Región Paracentral |

## Clientes

| Atributo | Tipo | #total | #nulos | #distintos | Media | Desv. | Moda | Mín. | Máx. |
|---|---|---|---|---|---|---|---|---|---|
| ClienteID | Nominal | 120 | 0 | 120 |  |  | CLI-0001 | CLI-0001 | CLI-0120 |
| Nombre | Nominal | 120 | 0 | 89 |  |  | José Rodríguez | Ana Flores | Valeria López |
| Segmento | Nominal | 120 | 0 | 3 |  |  | Pyme | Consumidor | Pyme |
| Region | Nominal | 120 | 0 | 4 |  |  | Región Occidental | Región Central | Región Paracentral |
| FechaRegistro | Nominal | 120 | 0 | 117 |  |  | 2019-05-29 | 2019-01-23 | 2024-03-13 |
| VisitasWeb2024 | Numérico | 120 | 0 | 107 | 211.45 | 119.92 | 12 | 7 | 395 |
| ConversionesWeb2024 | Numérico | 120 | 0 | 49 | 19.04 | 16.45 | 0 | 0 | 65 |

## Finanzas_Mensual

| Atributo | Tipo | #total | #nulos | #distintos | Media | Desv. | Moda | Mín. | Máx. |
|---|---|---|---|---|---|---|---|---|---|
| Mes | Nominal | 15 | 2 | 14 |  |  | Abril | Abril | Septiembre |
| Ingresos | Numérico | 15 | 3 | 13 | 194,289.55 | 25,921.88 | 169,484.80 | 169,484.80 | 258,969.71 |
| CostoVentas | Numérico | 15 | 3 | 13 | 113,527.11 | 16,020.26 | 97,483.15 | 97,483.15 | 155,230.40 |
| GastosOperativos | Numérico | 15 | 3 | 13 | 28,490.24 | 5,555.03 | 21,346.46 | 21,346.46 | 39,756.11 |
| UtilidadNeta | Numérico | 15 | 3 | 13 | 52,272.20 | 6,985.36 | 43,203.83 | 43,203.83 | 65,903.20 |
| FlujoCaja | Numérico | 15 | 3 | 13 | 37,576.47 | 5,400.49 | 26,346.22 | 26,346.22 | 45,504.65 |
| InversionesRealizadas | Numérico | 15 | 3 | 13 | 48,985.76 | 11,846.02 | 32,919.05 | 32,919.05 | 67,995.18 |
| RetornoInversion | Numérico | 15 | 3 | 13 | 1.11 | 0.22 | 0.77 | 0.77 | 1.43 |
