// Dim_Region: generado por `python -m etl.generar` desde etl/contrato.py
let
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Dim_Region"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Dim_Region.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            Encabezados = Table.PromoteHeaders(Csv, [PromoteAllScalars = true])
        in
            Table.TransformColumnTypes(Encabezados, {
        {"region_key", Int64.Type},
        {"region", type text}
            }, "en-US"),
    Resultado = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV()
in
    Resultado
