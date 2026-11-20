# Dashboard final en Power BI Desktop

## Preparación
Desde la raíz del proyecto ejecuta:

```powershell
python src/etl.py
python src/modelos.py
python src/no_supervisado.py
python src/export_powerbi.py
```

Después abre Power BI Desktop y usa **Obtener datos > Texto/CSV** para importar los archivos de `powerbi/data/`.

## Modelo de datos
Crea estas relaciones:

```text
dim_date[date_id]       1 --- * fact_rentals[date_id]
dim_time[time_id]       1 --- * fact_rentals[time_id]
dim_weather[weather_id] 1 --- * fact_rentals[weather_id]
```

## Páginas del dashboard
1. **Resumen ejecutivo**: total de rentas, promedio, máximo, registros, demanda por hora, temporada y clima.
2. **Comportamiento de la demanda**: hora, día, temporada, temperatura y días laborales.
3. **Modelos supervisados**: R², MAE, RMSE, Accuracy, Precision, Recall, F1 y matriz de confusión.
4. **Clustering y PCA**: Silhouette por k, perfiles de cluster y dispersión PCA.
5. **Conclusiones**: problema -> datos -> análisis -> conocimiento -> recomendaciones.

Guarda el archivo como:

```text
powerbi/Moya_MarkAlan_BikeSharing_Dashboard.pbix
```
