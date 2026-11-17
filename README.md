# Predicción de demanda en un sistema de bicicletas compartidas

Proyecto individual de recursamiento de la asignatura **Extracción de Conocimiento en Bases de Datos**.

**Alumno:** Mark Alan Moya Galindo  
**Proyecto:** No. 3  
**Dataset:** Bike Sharing  
**Fuente:** UCI Machine Learning Repository  
**Repositorio:** https://github.com/kamcr7/bike-sharing-demand

## Objetivo

Analizar el dataset Bike Sharing para identificar factores relacionados con la demanda de bicicletas y desarrollar un flujo completo de exploración, preparación, modelado supervisado, análisis no supervisado y visualización.

## Dataset

El análisis principal utiliza `hour.csv`, con **17,379 registros y 17 variables**. El dataset original permanece sin modificaciones en:

```text
data/raw/
├── hour.csv
├── day.csv
└── Readme.txt
```

## Estado del proyecto - corte del 17 de noviembre de 2026

### Unidad II - Exploración y diagnóstico
Completado:
- exploración con Pandas;
- diccionario de datos;
- faltantes y duplicados;
- inconsistencias y outliers;
- estadística descriptiva;
- visualizaciones;
- notebook e informe PDF.

### Unidad II - ETL y Data Mart
Implementado:
- `src/etl.py`
- `notebooks/02_limpieza_etl.ipynb`
- `data/processed/bike_sharing_clean.csv`
- `data/processed/bike_sharing_datamart.db`
- `docs/esquema_data_mart.md`
- `sql/datamart.sql`

### Unidad III - Análisis supervisado
Implementado:
- regresión lineal;
- Random Forest Regressor;
- regresión logística;
- Random Forest Classifier;
- métricas de regresión y clasificación;
- matriz de confusión;
- modelos serializados.

Archivos:
```text
src/modelos.py
notebooks/03_modelos_supervisados.ipynb
outputs/metricas/
outputs/modelos/
outputs/graficas/
```

### Unidad IV - Análisis no supervisado
Se agrega:
- estandarización de variables;
- K-Means;
- evaluación de k entre 2 y 8;
- método del codo;
- Silhouette Score;
- perfil de clusters;
- PCA con dos componentes;
- visualización de clusters.

Archivos:
```text
src/no_supervisado.py
notebooks/Moya_MarkAlan_U4_AnalisisNoSupervisado.ipynb
outputs/no_supervisado/
```

Variables:
```text
hr
weekday
season
weathersit
temp
hum
windspeed
cnt
```

## Dashboard
El dashboard se encuentra en:
```text
dashboard/app.py
```

Actualmente presenta datos, calidad, estadística descriptiva y visualizaciones. Para el cierre se continuará integrando resultados supervisados y no supervisados.

## Estructura principal

```text
bike-sharing-demand/
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── Moya_MarkAlan_U2_AE1_Exploracion.ipynb
│   ├── 02_limpieza_etl.ipynb
│   ├── 03_modelos_supervisados.ipynb
│   └── Moya_MarkAlan_U4_AnalisisNoSupervisado.ipynb
├── sql/
│   └── datamart.sql
├── src/
│   ├── etl.py
│   ├── modelos.py
│   └── no_supervisado.py
├── outputs/
├── dashboard/
├── docs/
└── requirements.txt
```

## Ejecución

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

ETL:
```powershell
python src/etl.py
```

Modelos supervisados:
```powershell
python src/modelos.py
```

Análisis no supervisado:
```powershell
python src/no_supervisado.py
```

Dashboard:
```powershell
python -m streamlit run dashboard/app.py
```

Jupyter:
```powershell
python -m jupyter notebook
```

## Metodología
El proyecto sigue CRISP-DM:
1. Comprensión del negocio.
2. Comprensión de los datos.
3. Preparación de los datos.
4. Modelado.
5. Evaluación.
6. Despliegue y documentación.

## Pregunta principal

**¿En qué medida la hora, el tipo de día, la temporada y las condiciones climáticas permiten predecir la cantidad total de bicicletas rentadas en el sistema Bike Sharing?**

## Fuente
Fanaee-T, H. (2013). *Bike Sharing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894
