# Diccionario de datos - Bike Sharing (hour.csv)

Archivo principal: `data/raw/hour.csv` — 17,379 registros y 17 variables.

| variable   | tipo_general       | descripcion                                                        | uso_propuesto                          |
|:-----------|:-------------------|:-------------------------------------------------------------------|:---------------------------------------|
| instant    | entero             | Índice del registro                                                | No usar como predictor                 |
| dteday     | fecha              | Fecha del registro                                                 | Análisis temporal                      |
| season     | categórica         | Temporada: 1 primavera, 2 verano, 3 otoño, 4 invierno              | Predictor                              |
| yr         | binaria            | Año: 0=2011, 1=2012                                                | Predictor                              |
| mnth       | categórica         | Mes, de 1 a 12                                                     | Predictor                              |
| hr         | categórica/ordinal | Hora del día, de 0 a 23                                            | Predictor                              |
| holiday    | binaria            | Indica si el día es festivo                                        | Predictor                              |
| weekday    | categórica         | Día de la semana                                                   | Predictor                              |
| workingday | binaria            | 1 si no es fin de semana ni festivo; 0 en otro caso                | Predictor                              |
| weathersit | categórica         | Situación climática codificada de 1 a 4                            | Predictor                              |
| temp       | continua           | Temperatura normalizada; valor original dividido entre 41          | Predictor                              |
| atemp      | continua           | Sensación térmica normalizada; valor original dividido entre 50    | Predictor                              |
| hum        | continua           | Humedad normalizada; valor original dividido entre 100             | Predictor                              |
| windspeed  | continua           | Velocidad del viento normalizada; valor original dividido entre 67 | Predictor                              |
| casual     | entero             | Cantidad de usuarios casuales                                      | Descriptiva; no usar para predecir cnt |
| registered | entero             | Cantidad de usuarios registrados                                   | Descriptiva; no usar para predecir cnt |
| cnt        | entero             | Cantidad total de bicicletas rentadas                              | Variable objetivo de regresión         |
