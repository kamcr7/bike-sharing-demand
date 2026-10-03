Predicción de demanda en un sistema de bicicletas compartidas
Proyecto individual de recursamiento de la asignatura Extracción de Conocimiento en Bases de Datos.
Alumno: Mark Alan Moya Galindo
Proyecto: No. 3
Dataset: Bike Sharing
Fuente: UCI Machine Learning Repository
Repositorio: https://github.com/kamcr7/bike-sharing-demand
Objetivo del proyecto
Analizar el conjunto de datos Bike Sharing para identificar los factores relacionados con la demanda de bicicletas y preparar modelos que permitan estimar la cantidad de rentas y clasificar niveles de demanda.
Dataset
El dataset Bike Sharing contiene información horaria y diaria del sistema Capital Bikeshare para 2011 y 2012, junto con variables de tiempo, calendario y clima.
Para el análisis principal se utilizará hour.csv, que contiene aproximadamente 17,389 registros. La variable principal a predecir será cnt, que representa el total de bicicletas rentadas.
Archivos originales
Los archivos originales deben conservarse sin modificaciones en:
data/raw/
├── hour.csv
├── day.csv
└── Readme.txt
Estructura propuesta
bike-sharing-demand/
├── data/
│   └── raw/
│       ├── hour.csv
│       ├── day.csv
│       └── Readme.txt
├── notebooks/
├── src/
├── outputs/
├── README.md
└── .gitignore
Variables de interés
Entre las variables que se analizarán se encuentran:
- hr: hora del día.
- weekday: día de la semana.
- workingday: indica si es día laboral.
- holiday: indica si es día festivo.
- season: temporada del año.
- mnth: mes.
- weathersit: condición general del clima.
- temp: temperatura normalizada.
- atemp: sensación térmica normalizada.
- hum: humedad normalizada.
- windspeed: velocidad del viento normalizada.
- cnt: cantidad total de bicicletas rentadas.
casual y registered se usarán principalmente para descripción, pero no como predictores directos de cnt, ya que cnt corresponde a la suma de ambos conteos.
Análisis planeado
Regresión
Predecir la cantidad total de bicicletas rentadas (cnt) utilizando variables temporales, de calendario y climáticas.
Clasificación
Crear una variable derivada de nivel de demanda con tres categorías: baja, media y alta. Como criterio preliminar se usarán los percentiles 33 y 67 calculados sobre los datos de entrenamiento.
Análisis no supervisado
Explorar agrupamientos que permitan identificar perfiles de uso relacionados con horarios y condiciones climáticas.
Metodología
El proyecto seguirá CRISP-DM:
1. Comprensión del negocio.
2. Comprensión de los datos.
3. Preparación de los datos.
4. Modelado.
5. Evaluación.
6. Despliegue/documentación.
Herramientas propuestas
- Python
- pandas
- NumPy
- Matplotlib
- scikit-learn
- Jupyter Notebook o Visual Studio Code
- SQLite
- Git y GitHub
Pregunta principal
¿En qué medida la hora, el tipo de día, la temporada y las condiciones climáticas permiten predecir la cantidad total de bicicletas rentadas en el sistema Bike Sharing?
Fuente del dataset
Fanaee-T, H. (2013). Bike Sharing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894
