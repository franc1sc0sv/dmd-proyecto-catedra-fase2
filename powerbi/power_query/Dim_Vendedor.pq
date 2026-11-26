// Dim_Vendedor: generado por `python -m etl.generar` desde etl/contrato.py
// Mismas columnas y mismos tipos desde CSV o desde SQL Server (los tipos se fijan al final en ambos casos).
let
    Tipos = {
        {"vendedor_key", Int64.Type},
        {"equipo", type text}
    },
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Dim_Vendedor"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Dim_Vendedor.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv])
        in
            Table.PromoteHeaders(Csv, [PromoteAllScalars = true]),
    Origen = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV(),
    Resultado = Table.TransformColumnTypes(Table.SelectColumns(Origen, List.Transform(Tipos, each _{0})), Tipos, "en-US")
in
    Resultado
