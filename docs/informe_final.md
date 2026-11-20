# Informe final — borrador

## Proyecto
Predicción de demanda en un sistema de bicicletas compartidas

## Alumno
Mark Alan Moya Galindo

## Resumen
El proyecto analiza el dataset Bike Sharing de UCI mediante exploración, preparación de datos, ETL, Data Mart, modelos supervisados, análisis no supervisado y visualización final en Power BI Desktop.

## Datos y preparación
El análisis principal utiliza hour.csv con 17,379 registros y 17 variables. Se confirmó ausencia de valores faltantes y duplicados completos. El dataset original se conserva intacto en data/raw/.

## ETL y Data Mart
El ETL extrae, valida, transforma y carga los datos. Se genera un dataset procesado y un Data Mart SQLite con fact_rentals, dim_date, dim_time y dim_weather.

## Modelos supervisados
Random Forest Regressor fue el mejor modelo de regresión con R² ≈ 0.943843, MAE ≈ 25.121 y RMSE ≈ 42.169. Random Forest Classifier fue el mejor modelo de clasificación con Accuracy ≈ 0.877445 y F1 ≈ 0.879206.

## Análisis no supervisado
K-Means fue evaluado entre k=2 y k=8. El mejor resultado fue k=4 con Silhouette ≈ 0.177637. PCA permitió representar los grupos en dos dimensiones y las dos primeras componentes explicaron aproximadamente 43.90 % de la variación.

## Dashboard Power BI
El dashboard final integra indicadores generales, visualizaciones descriptivas, resultados supervisados, clustering y PCA, siguiendo un storytelling de problema -> datos -> análisis -> conocimiento -> recomendaciones.

## Conclusión
La demanda presenta patrones temporales y climáticos relevantes. Random Forest ofreció el mejor desempeño predictivo y K-Means permitió identificar cuatro perfiles de comportamiento.

## Recomendación
Los resultados pueden apoyar la planificación de disponibilidad y redistribución de bicicletas según horario, temporada y clima.
