from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "bike_sharing_datamart.db"
OUT = ROOT / "powerbi" / "data"
OUT.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(DB) as con:
    for table in ["fact_rentals", "dim_date", "dim_time", "dim_weather"]:
        df = pd.read_sql_query(f"SELECT * FROM {table}", con)
        df.to_csv(OUT / f"{table}.csv", index=False, encoding="utf-8-sig")
        print(f"{table}: {len(df):,} filas")

extras = [
    ROOT/"outputs/metricas/regresion_metricas.csv",
    ROOT/"outputs/metricas/clasificacion_metricas.csv",
    ROOT/"outputs/metricas/matriz_confusion_clasificacion.csv",
    ROOT/"outputs/no_supervisado/resumen_clusters.csv",
    ROOT/"outputs/no_supervisado/kmeans_evaluacion.csv",
    ROOT/"outputs/no_supervisado/pca_componentes.csv",
    ROOT/"outputs/no_supervisado/bike_sharing_clusters.csv",
]
for src in extras:
    if src.exists():
        pd.read_csv(src).to_csv(OUT/src.name, index=False, encoding="utf-8-sig")
        print("Exportado:", src.name)

print("Listo. Archivos de Power BI en", OUT)
