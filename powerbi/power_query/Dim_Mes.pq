// Dim_Mes: generado por `python -m etl.generar` desde etl/contrato.py
// Mismas columnas y mismos tipos desde CSV o desde SQL Server (los tipos se fijan al final en ambos casos).
let
    Tipos = {
        {"mes_key", Int64.Type},
        {"mes_numero", Int64.Type},
        {"nombre_mes", type text},
        {"trimestre", Int64.Type},
        {"semestre", Int64.Type},
        {"anio", Int64.Type}
    },
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Dim_Mes"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Dim_Mes.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv])
        in
            Table.PromoteHeaders(Csv, [PromoteAllScalars = true]),
    Origen = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV(),
    Resultado = Table.TransformColumnTypes(Table.SelectColumns(Origen, List.Transform(Tipos, each _{0})), Tipos, "en-US")
in
    Resultado
