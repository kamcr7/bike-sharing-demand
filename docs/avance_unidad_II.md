# Avance Unidad II - Preparación de datos

## Exploración inicial
- `hour.csv`: 17,379 registros y 17 variables.
- Valores faltantes: 0.
- Filas duplicadas: 0.
- Variable objetivo principal: `cnt`.

## Limpieza inicial
El dataset original no presenta valores faltantes ni filas duplicadas. Se conserva sin modificaciones en `data/raw/`.

## Transformaciones ETL
Se genera `data/processed/bike_sharing_clean.csv` con variables derivadas de fecha y versiones interpretables de temperatura, sensación térmica, humedad y viento.

## Data Mart
Se construye `data/processed/bike_sharing_datamart.db` con un esquema estrella formado por `dim_date`, `dim_time`, `dim_weather` y `fact_rentals`.

## Consideración de fuga de información
`casual` y `registered` se mantienen para análisis descriptivo, pero se excluyen de los modelos que predicen `cnt`, ya que `cnt = casual + registered`.
