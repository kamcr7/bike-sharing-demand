from pathlib import Path
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = ROOT / "data" / "processed" / "bike_sharing_clean.csv"
DATA_RAW = ROOT / "data" / "raw" / "hour.csv"

OUT = ROOT / "outputs" / "no_supervisado"
PLOTS = OUT / "graficas"
MODELS = OUT / "modelos"
for path in (OUT, PLOTS, MODELS):
    path.mkdir(parents=True, exist_ok=True)

FEATURES = ["hr","weekday","season","weathersit","temp","hum","windspeed","cnt"]

def cargar_datos():
    path = DATA_PROCESSED if DATA_PROCESSED.exists() else DATA_RAW
    if not path.exists():
        raise FileNotFoundError("No se encontro el dataset procesado ni data/raw/hour.csv")
    df = pd.read_csv(path)
    print(f"Dataset utilizado: {path}")
    print(f"Registros: {len(df):,}")
    return df

def evaluar_kmeans(X_scaled):
    filas = []
    for k in range(2, 9):
        modelo = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = modelo.fit_predict(X_scaled)
        sil = silhouette_score(
            X_scaled, labels,
            sample_size=min(5000, len(X_scaled)),
            random_state=42
        )
        filas.append({"k": k, "inercia": float(modelo.inertia_), "silhouette": float(sil)})
    return pd.DataFrame(filas)

def main():
    df = cargar_datos()
    X = df[FEATURES].copy()

    if X.isna().sum().sum():
        raise ValueError("Las variables seleccionadas contienen valores faltantes")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    metricas = evaluar_kmeans(X_scaled)
    metricas.to_csv(OUT / "kmeans_evaluacion.csv", index=False)

    mejor_k = int(metricas.loc[metricas["silhouette"].idxmax(), "k"])
    kmeans = KMeans(n_clusters=mejor_k, random_state=42, n_init=20)
    labels = kmeans.fit_predict(X_scaled)

    resultado = X.copy()
    resultado["cluster"] = labels
    resultado.to_csv(OUT / "bike_sharing_clusters.csv", index=False)

    resumen = (
        resultado.groupby("cluster")
        .agg(
            registros=("cluster","size"),
            hora_promedio=("hr","mean"),
            demanda_promedio=("cnt","mean"),
            temperatura_promedio=("temp","mean"),
            humedad_promedio=("hum","mean"),
            viento_promedio=("windspeed","mean"),
            clima_promedio=("weathersit","mean"),
            temporada_promedio=("season","mean"),
        )
        .reset_index()
    )
    resumen.to_csv(OUT / "resumen_clusters.csv", index=False)

    fig, ax1 = plt.subplots(figsize=(8,5))
    ax1.plot(metricas["k"], metricas["inercia"], marker="o")
    ax1.set_xlabel("Numero de clusters (k)")
    ax1.set_ylabel("Inercia")
    ax2 = ax1.twinx()
    ax2.plot(metricas["k"], metricas["silhouette"], marker="s")
    ax2.set_ylabel("Silhouette Score")
    plt.title("Evaluacion de K-Means")
    fig.tight_layout()
    plt.savefig(PLOTS / "kmeans_codo_silhouette.png", dpi=160)
    plt.close()

    pca = PCA(n_components=2)
    comps = pca.fit_transform(X_scaled)
    pca_df = pd.DataFrame(comps, columns=["PC1","PC2"])
    pca_df["cluster"] = labels
    pca_df.to_csv(OUT / "pca_componentes.csv", index=False)

    plt.figure(figsize=(8,6))
    for c in sorted(pca_df["cluster"].unique()):
        sub = pca_df[pca_df["cluster"] == c]
        plt.scatter(sub["PC1"], sub["PC2"], s=9, alpha=.45, label=f"Cluster {c}")
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var.)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var.)")
    plt.title("Clusters representados con PCA")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS / "clusters_pca.png", dpi=160)
    plt.close()

    joblib.dump(scaler, MODELS / "standard_scaler.joblib")
    joblib.dump(kmeans, MODELS / "kmeans_modelo.joblib")
    joblib.dump(pca, MODELS / "pca_modelo.joblib")

    resumen_json = {
        "variables": FEATURES,
        "mejor_k": mejor_k,
        "silhouette_mejor_k": float(metricas.loc[metricas["k"] == mejor_k, "silhouette"].iloc[0]),
        "pca_varianza_explicada_pc1": float(pca.explained_variance_ratio_[0]),
        "pca_varianza_explicada_pc2": float(pca.explained_variance_ratio_[1]),
        "pca_varianza_explicada_total_2_componentes": float(pca.explained_variance_ratio_.sum()),
    }
    with open(OUT / "resumen_no_supervisado.json","w",encoding="utf-8") as f:
        json.dump(resumen_json,f,indent=2,ensure_ascii=False)

    print(metricas.to_string(index=False))
    print(f"\nMejor k: {mejor_k}")
    print("\nResumen de clusters:")
    print(resumen.round(3).to_string(index=False))
    print("\nResultados guardados en:", OUT)

if __name__ == "__main__":
    main()
