// Hecho_Finanzas_Mensual: generado por `python -m etl.generar` desde etl/contrato.py
let
    DesdeSQL = () => Sql.Database(Servidor, BaseDatos){[Schema = "dbo", Item = "Hecho_Finanzas_Mensual"]}[Data],
    DesdeCSV = () =>
        let
            Csv = Csv.Document(File.Contents(CarpetaMuestra & "\Hecho_Finanzas_Mensual.csv"),
                               [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            Encabezados = Table.PromoteHeaders(Csv, [PromoteAllScalars = true])
        in
            Table.TransformColumnTypes(Encabezados, {
        {"mes_key", Int64.Type},
        {"ingresos", Currency.Type},
        {"costo_ventas", Currency.Type},
        {"gastos_operativos", Currency.Type},
        {"utilidad_neta", Currency.Type},
        {"flujo_caja", Currency.Type},
        {"inversiones_realizadas", Currency.Type},
        {"retorno_inversion", type number}
            }, "en-US"),
    Resultado = if FuenteDatos = "SQL" then DesdeSQL() else DesdeCSV()
in
    Resultado
