# Datos

## `raw/`
`datos_andina_retail_corp.xlsx`: el archivo original del Aula Digital, sin modificar. Está en Git porque es pequeño (75 KB) y la propia hoja de Finanzas lo declara *"Datos simulados con fines académicos"*.

SHA256: `7e9568e2704317a3ae3cdaaccfa0a6c8e7cdbac1d1ca922c02060578e5fa7a8a`. El ETL avisa si el archivo cambia.

Hojas: Ventas (850 × 11), Clientes (120 × 7), Finanzas_Mensual (12 × 8, más 2 filas vacías y una nota). Contexto solo describe el caso y no se carga.

## `sample/`
**Lo genera el ETL; no editar a mano.** Un CSV por tabla del contrato (UTF-8 con BOM, fechas `AAAA-MM-DD`, punto decimal), con las mismas llaves que la BD. Es el extracto **completo**, no un subconjunto.

`perfil_atributos.md` es el perfilado del Excel antes de limpiar. `reporte_carga.md` documenta la última carga: conciliación, rechazos y observaciones.
