// Hecho_Trafico_Web: generado por `python -m etl.generar` desde etl/contrato.py
// Mismas columnas y mismos tipos desde CSV o desde SQL Server (los tipos se fijan al final en ambos casos).
let
    Tipos = {
        {"cliente_key", Int64.Type},
        {"region_cliente_key", Int64.Type},
        {"anio", Int64.Type},
        {"visitas_web", Int64.Type},
        {"conversiones_web", Int64.Type}
    },
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Hecho_Trafico_Web"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Hecho_Trafico_Web.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv])
        in
            Table.PromoteHeaders(Csv, [PromoteAllScalars = true]),
    Origen = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV(),
    Resultado = Table.TransformColumnTypes(Table.SelectColumns(Origen, List.Transform(Tipos, each _{0})), Tipos, "en-US")
in
    Resultado
