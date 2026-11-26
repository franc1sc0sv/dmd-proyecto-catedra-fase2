// Dim_Tiempo: generado por `python -m etl.generar` desde etl/contrato.py
let
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Dim_Tiempo"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Dim_Tiempo.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            Encabezados = Table.PromoteHeaders(Csv, [PromoteAllScalars = true])
        in
            Table.TransformColumnTypes(Encabezados, {
        {"tiempo_key", Int64.Type},
        {"fecha", type date},
        {"dia_semana", type text},
        {"mes_numero", Int64.Type},
        {"nombre_mes", type text},
        {"trimestre", Int64.Type},
        {"semestre", Int64.Type},
        {"anio", Int64.Type},
        {"mes_key", Int64.Type}
            }, "en-US"),
    Resultado = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV()
in
    Resultado
