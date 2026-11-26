// Hecho_Ventas: generado por `python -m etl.generar` desde etl/contrato.py
let
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Hecho_Ventas"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Hecho_Ventas.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            Encabezados = Table.PromoteHeaders(Csv, [PromoteAllScalars = true])
        in
            Table.TransformColumnTypes(Encabezados, {
        {"tiempo_key", Int64.Type},
        {"mes_key", Int64.Type},
        {"cliente_key", Int64.Type},
        {"producto_key", Int64.Type},
        {"canal_key", Int64.Type},
        {"vendedor_key", Int64.Type},
        {"region_cliente_key", Int64.Type},
        {"region_venta_key", Int64.Type},
        {"orden_id", type text},
        {"cantidad", Int64.Type},
        {"precio_unitario", Currency.Type},
        {"total", Currency.Type}
            }, "en-US"),
    Resultado = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV()
in
    Resultado
