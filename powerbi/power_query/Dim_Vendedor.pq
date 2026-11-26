// Dim_Vendedor: generado por `python -m etl.generar` desde etl/contrato.py
let
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Dim_Vendedor"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Dim_Vendedor.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            Encabezados = Table.PromoteHeaders(Csv, [PromoteAllScalars = true])
        in
            Table.TransformColumnTypes(Encabezados, {
        {"vendedor_key", Int64.Type},
        {"equipo", type text}
            }, "en-US"),
    Resultado = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV()
in
    Resultado
