// Hecho_Trafico_Web: generado por `python -m etl.generar` desde etl/contrato.py
let
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Hecho_Trafico_Web"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Hecho_Trafico_Web.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            Encabezados = Table.PromoteHeaders(Csv, [PromoteAllScalars = true])
        in
            Table.TransformColumnTypes(Encabezados, {
        {"cliente_key", Int64.Type},
        {"region_cliente_key", Int64.Type},
        {"anio", Int64.Type},
        {"visitas_web", Int64.Type},
        {"conversiones_web", Int64.Type}
            }, "en-US"),
    Resultado = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV()
in
    Resultado
