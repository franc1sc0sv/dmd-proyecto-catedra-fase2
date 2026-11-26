"""Rutas del proyecto y conexión a SQL Server (leída de .env)."""

import os
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

EXCEL = RAIZ / "data" / "raw" / "datos_andina_retail_corp.xlsx"
EXCEL_SHA256 = "7e9568e2704317a3ae3cdaaccfa0a6c8e7cdbac1d1ca922c02060578e5fa7a8a"
SAMPLE = RAIZ / "data" / "sample"
SQL_DIR = RAIZ / "sql"
# Resultado de K-means (parte 3). Si existe, el ETL lo usa para llenar Dim_Cliente.segmento_cluster.
SEGMENTOS = RAIZ / "mining" / "output" / "segmentos_cliente.csv"

DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "AndinaRetailDW")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_TRUST_CERT = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes")


def odbc_string(database: str | None = None) -> str:
    partes = [
        f"DRIVER={{{DB_DRIVER}}}",
        f"SERVER={DB_SERVER}",
        f"DATABASE={database or DB_NAME}",
        f"TrustServerCertificate={DB_TRUST_CERT}",
    ]
    if DB_USER:
        partes += [f"UID={DB_USER}", f"PWD={DB_PASSWORD}"]
    else:
        partes.append("Trusted_Connection=yes")
    return ";".join(partes)


def sqlalchemy_url(database: str | None = None) -> str:
    return "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(odbc_string(database))
