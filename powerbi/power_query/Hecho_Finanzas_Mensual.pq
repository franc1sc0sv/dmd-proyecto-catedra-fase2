// Hecho_Finanzas_Mensual: generado por `python -m etl.generar` desde etl/contrato.py
// Mismas columnas y mismos tipos desde CSV o desde SQL Server (los tipos se fijan al final en ambos casos).
let
    Tipos = {
        {"mes_key", Int64.Type},
        {"ingresos", Currency.Type},
        {"costo_ventas", Currency.Type},
        {"gastos_operativos", Currency.Type},
        {"utilidad_neta", Currency.Type},
        {"flujo_caja", Currency.Type},
        {"inversiones_realizadas", Currency.Type},
        {"retorno_inversion", type number}
    },
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Hecho_Finanzas_Mensual"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Hecho_Finanzas_Mensual.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv])
        in
            Table.PromoteHeaders(Csv, [PromoteAllScalars = true]),
    Origen = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV(),
    Resultado = Table.TransformColumnTypes(Table.SelectColumns(Origen, List.Transform(Tipos, each _{0})), Tipos, "en-US")
in
    Resultado
