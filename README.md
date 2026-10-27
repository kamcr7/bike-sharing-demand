# Predicción de demanda en un sistema de bicicletas compartidas

Proyecto individual de recursamiento de la asignatura **Extracción de Conocimiento en Bases de Datos**.

**Alumno:** Mark Alan Moya Galindo  
**Proyecto:** No. 3  
**Dataset:** Bike Sharing  
**Fuente:** UCI Machine Learning Repository  
**Repositorio:** https://github.com/kamcr7/bike-sharing-demand

## Objetivo del proyecto

Analizar el conjunto de datos Bike Sharing para identificar los factores relacionados con la demanda de bicicletas y desarrollar modelos que permitan estimar la cantidad de rentas y clasificar niveles de demanda.

## Dataset

El dataset Bike Sharing contiene información horaria y diaria del sistema Capital Bikeshare para 2011 y 2012, junto con variables temporales, de calendario y clima.

Para el análisis principal se utiliza `hour.csv`, con **17,379 registros y 17 variables**. La variable principal a predecir es `cnt`, que representa el total de bicicletas rentadas.

Los archivos originales se conservan sin modificaciones en:

```text
data/raw/
├── hour.csv
├── day.csv
└── Readme.txt
```

## Estructura actual del proyecto

```text
bike-sharing-demand/
├── data/
│   ├── raw/
│   │   ├── hour.csv
│   │   ├── day.csv
│   │   └── Readme.txt
│   └── processed/
│       ├── bike_sharing_clean.csv
│       └── bike_sharing_datamart.db
├── docs/
│   ├── diccionario_datos.csv
│   ├── diccionario_datos.md
│   ├── esquema_data_mart.md
│   ├── avance_unidad_II.md
│   └── revision_unidad_III_23_octubre.md
├── notebooks/
│   ├── 01_exploracion_datos.ipynb
│   ├── 02_limpieza_etl.ipynb
│   └── 03_modelos_supervisados.ipynb
├── outputs/
│   ├── graficas/
│   ├── metricas/
│   ├── modelos/
│   ├── estadisticas_descriptivas_hour.csv
│   ├── calidad_datos_hour.csv
│   └── validacion_datos.csv
├── src/
│   ├── etl.py
│   └── modelos.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Avance conforme al calendario hasta el 23 de octubre de 2026

### Unidad I - Planeación

Se definieron el problema, la pregunta principal, los objetivos, alcance, herramientas, metodología CRISP-DM y las tareas de regresión, clasificación y análisis no supervisado.

### Unidad II - Preparación de datos

Se completaron:

- Diccionario de datos.
- Exploración inicial y estadísticas descriptivas.
- Revisión de valores faltantes y duplicados.
- Proceso ETL reproducible en `src/etl.py`.
- Dataset procesado en `data/processed/bike_sharing_clean.csv`.
- Data Mart en SQLite: `data/processed/bike_sharing_datamart.db`.
- Esquema estrella documentado en `docs/esquema_data_mart.md`.

El dataset original no presenta valores faltantes ni filas duplicadas.

### Revisión Unidad III - 23 de octubre

Se implementaron modelos supervisados preliminares en `src/modelos.py`.

#### Regresión

Variable objetivo: `cnt`.

Variables predictoras iniciales:

- `hr`
- `weekday`
- `workingday`
- `holiday`
- `season`
- `mnth`
- `yr`
- `weathersit`
- `temp`
- `atemp`
- `hum`
- `windspeed`

`casual` y `registered` no se utilizan como predictores de `cnt`, porque `cnt = casual + registered` y su uso produciría fuga de información.

Resultados preliminares:

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| Regresión lineal | 104.80 | 139.21 | 0.388 |
| Random Forest Regressor | 25.12 | 42.17 | **0.944** |

#### Clasificación

Se creó conceptualmente el nivel de demanda con tres clases: **baja, media y alta**. Los límites se calculan únicamente con los datos de entrenamiento mediante los percentiles 33 y 67.

Umbrales obtenidos en la ejecución actual:

- Baja: `cnt <= 69`
- Media: `69 < cnt <= 228`
- Alta: `cnt > 228`

Resultados preliminares:

| Modelo | Accuracy | Precision macro | Recall macro | F1 macro |
|---|---:|---:|---:|---:|
| Regresión logística | 0.643 | 0.639 | 0.648 | 0.639 |
| Random Forest Classifier | **0.877** | **0.880** | **0.879** | **0.879** |

Estos modelos cumplen el objetivo de la **revisión del 23 de octubre: regresión y clasificación funcionando**. La evaluación y optimización completa corresponde a la entrega evaluable del 30 de octubre.

## Ejecución

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar ETL:

```bash
python src/etl.py
```

Ejecutar modelos:

```bash
python src/modelos.py
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

## Fuente del dataset

Fanaee-T, H. (2013). *Bike Sharing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894
