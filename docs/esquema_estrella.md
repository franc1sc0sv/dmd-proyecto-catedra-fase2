# Esquema estrella

Tres estrellas, una por proceso de negocio, con dimensiones compartidas (Fase 1, sección 5.1). Columnas, tipos y descripciones: [diccionario_datos.md](diccionario_datos.md). Diagrama original de la Fase 1: [esquema_estrella_fase1.png](esquema_estrella_fase1.png).

```mermaid
erDiagram
    Dim_Mes ||--o{ Hecho_Ventas : "mes_key"
    Dim_Mes ||--o{ Hecho_Finanzas_Mensual : "mes_key"
    Dim_Tiempo ||--o{ Hecho_Ventas : "tiempo_key"
    Dim_Cliente ||--o{ Hecho_Ventas : "cliente_key"
    Dim_Producto ||--o{ Hecho_Ventas : "producto_key"
    Dim_Canal ||--o{ Hecho_Ventas : "canal_key"
    Dim_Vendedor ||--o{ Hecho_Ventas : "vendedor_key"
    Dim_Region ||--o{ Hecho_Ventas : "region_venta_key"
    Dim_Region ||--o{ Hecho_Ventas : "region_cliente_key"
    Dim_Cliente ||--o{ Hecho_Trafico_Web : "cliente_key"
    Dim_Region ||--o{ Hecho_Trafico_Web : "region_cliente_key"

    Hecho_Ventas {
        int tiempo_key PK,FK
        int mes_key FK
        int cliente_key PK,FK
        int producto_key PK,FK
        int canal_key PK,FK
        int vendedor_key PK,FK
        int region_cliente_key PK,FK
        int region_venta_key PK,FK
        nvarchar orden_id PK "dimensión degenerada"
        int cantidad
        decimal precio_unitario
        decimal total
    }
    Hecho_Finanzas_Mensual {
        int mes_key PK,FK
        decimal ingresos
        decimal costo_ventas
        decimal gastos_operativos
        decimal utilidad_neta
        decimal flujo_caja
        decimal inversiones_realizadas
        decimal retorno_inversion
    }
    Hecho_Trafico_Web {
        int cliente_key PK,FK
        int region_cliente_key FK
        smallint anio PK "dimensión degenerada"
        int visitas_web
        int conversiones_web
    }
    Dim_Tiempo {
        int tiempo_key PK "AAAAMMDD"
        date fecha
        nvarchar dia_semana
        tinyint mes_numero
        nvarchar nombre_mes
        tinyint trimestre
        tinyint semestre
        smallint anio
    }
    Dim_Mes {
        int mes_key PK "AAAAMM"
        tinyint mes_numero
        nvarchar nombre_mes
        tinyint trimestre
        tinyint semestre
        smallint anio
    }
    Dim_Cliente {
        int cliente_key PK
        nvarchar cliente_id
        nvarchar nombre
        nvarchar segmento
        date fecha_registro
        int segmento_cluster "K-means"
    }
    Dim_Producto {
        int producto_key PK
        nvarchar producto
        nvarchar categoria
    }
    Dim_Canal {
        int canal_key PK
        nvarchar canal
    }
    Dim_Vendedor {
        int vendedor_key PK
        nvarchar equipo
    }
    Dim_Region {
        int region_key PK
        nvarchar region
    }
```

## Grano y volumen

| Tabla | Grano | Tipo (Clase 5) | Filas 2024 |
|---|---|---|---|
| Hecho_Ventas | Una orden (un producto por orden) | Transaction fact table | 850 |
| Hecho_Finanzas_Mensual | Un mes | Periodic snapshot | 12 |
| Hecho_Trafico_Web | Un cliente por año | Periodic snapshot | 120 |
| Dim_Tiempo / Dim_Mes | Un día / un mes | SCD 0 / conformada | 366 / 12 |
| Dim_Cliente / Dim_Producto / Dim_Canal / Dim_Vendedor | Un miembro | SCD tipo 1 | 120 / 20 / 2 / 5 |
| Dim_Region | Una región | Role-playing, SCD tipo 1 | 4 |

Dimensiones degeneradas: `orden_id` (Hecho_Ventas) y `anio` (Hecho_Trafico_Web). Es un **esquema estrella puro** (Clases 3 y 5): las dimensiones solo se relacionan con los hechos, nunca entre sí. `Dim_Mes` es la dimensión conformada que comparten Ventas y Finanzas para compararlas por mes.

Jerarquías: Tiempo `anio → semestre → trimestre → mes → día`; Producto `categoria → producto`.

Más tablas de control fuera del modelo dimensional: `Etl_Rechazos` y `Etl_Observaciones`.

## Cambios respecto a la Fase 1

Ver [decisiones.md](decisiones.md). En el esquema: `Hecho_Ventas` gana la columna `mes_key` (FK a la dimensión conformada `Dim_Mes`) y las llaves sustitutas son deterministas en lugar de IDENTITY.
