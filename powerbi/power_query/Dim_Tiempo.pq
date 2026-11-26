// Dim_Tiempo: generado por `python -m etl.generar` desde etl/contrato.py
// Mismas columnas y mismos tipos desde CSV o desde SQL Server (los tipos se fijan al final en ambos casos).
let
    Tipos = {
        {"tiempo_key", Int64.Type},
        {"fecha", type date},
        {"dia_semana", type text},
        {"mes_numero", Int64.Type},
        {"nombre_mes", type text},
        {"trimestre", Int64.Type},
        {"semestre", Int64.Type},
        {"anio", Int64.Type}
    },
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Dim_Tiempo"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Dim_Tiempo.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv])
        in
            Table.PromoteHeaders(Csv, [PromoteAllScalars = true]),
    Origen = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV(),
    Resultado = Table.TransformColumnTypes(Table.SelectColumns(Origen, List.Transform(Tipos, each _{0})), Tipos, "en-US")
in
    Resultado
