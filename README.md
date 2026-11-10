# Prediccion de demanda en un sistema de bicicletas compartidas

Proyecto individual de recursamiento de la asignatura **Extraccion de Conocimiento en Bases de Datos**.

**Alumno:** Mark Alan Moya Galindo  
**Proyecto:** No. 3  
**Dataset:** Bike Sharing  
**Fuente:** UCI Machine Learning Repository  
**Repositorio:** https://github.com/kamcr7/bike-sharing-demand

## Objetivo del proyecto

Analizar el conjunto de datos Bike Sharing para identificar los factores relacionados con la demanda de bicicletas y preparar modelos que permitan estimar la cantidad de rentas y clasificar niveles de demanda.

## Dataset

El dataset Bike Sharing contiene informacion horaria y diaria del sistema Capital Bikeshare para los anios 2011 y 2012, junto con variables relacionadas con tiempo, calendario y clima.

Para el analisis principal se utiliza `hour.csv`, que contiene **17,379 registros y 17 variables**.

La variable principal a predecir sera `cnt`, que representa el total de bicicletas rentadas.

## Archivos originales

Los archivos originales se conservan sin modificaciones en:

```text
data/raw/
├── hour.csv
├── day.csv
└── Readme.txt
```

## Variables de interes

- `hr`: hora del dia.
- `weekday`: dia de la semana.
- `workingday`: indica si es dia laboral.
- `holiday`: indica si es dia festivo.
- `season`: temporada del anio.
- `mnth`: mes.
- `weathersit`: condicion general del clima.
- `temp`: temperatura normalizada.
- `atemp`: sensacion termica normalizada.
- `hum`: humedad normalizada.
- `windspeed`: velocidad del viento normalizada.
- `cnt`: cantidad total de bicicletas rentadas.

Las variables `casual` y `registered` se utilizan principalmente para descripcion, pero no como predictores directos de `cnt`, ya que `cnt` corresponde a la suma de ambos conteos.

## Analisis planeado

### Regresion
Predecir la cantidad total de bicicletas rentadas (`cnt`) utilizando variables temporales, de calendario y climaticas.

### Clasificacion
Crear posteriormente una variable derivada de nivel de demanda con tres categorias: baja, media y alta. Los puntos de corte se documentaran antes del modelado.

### Analisis no supervisado
Explorar agrupamientos que permitan identificar perfiles de uso relacionados con horarios y condiciones climaticas.

## Metodologia

El proyecto sigue CRISP-DM:
1. Comprension del negocio.
2. Comprension de los datos.
3. Preparacion de los datos.
4. Modelado.
5. Evaluacion.
6. Despliegue y documentacion.

## Unidad II - Actividad de Evaluacion 1

Esta actividad realiza la **exploracion y diagnostico del dataset original**, sin modificar `data/raw/hour.csv`.

Evidencias agregadas:

```text
notebooks/Moya_MarkAlan_U2_AE1_Exploracion.ipynb
docs/Moya_MarkAlan_U2_AE1_Diagnostico.pdf
docs/diccionario_datos_U2_AE1.csv
dashboard/app.py
outputs/u2_ae1/
```

Incluye:
- carga y exploracion con Pandas;
- numero de registros y variables;
- diccionario de datos;
- clasificacion de variables;
- tipo y fuente de los datos;
- valores faltantes y duplicados;
- validaciones de consistencia;
- deteccion inicial de valores atipicos;
- estadistica descriptiva;
- visualizaciones;
- propuestas para regresion, clasificacion y agrupamiento;
- dashboard interactivo.

### Ejecutar el notebook

Abre `notebooks/Moya_MarkAlan_U2_AE1_Exploracion.ipynb` en VS Code o Jupyter y ejecuta todas las celdas.

### Ejecutar el dashboard

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Pregunta principal

¿En que medida la hora, el tipo de dia, la temporada y las condiciones climaticas permiten predecir la cantidad total de bicicletas rentadas en el sistema Bike Sharing?

## Fuente del dataset

Fanaee-T, H. (2013). *Bike Sharing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894
