# Predicción de demanda en un sistema de bicicletas compartidas

Proyecto individual de recursamiento de **Extracción de Conocimiento en Bases de Datos**.

**Alumno:** Mark Alan Moya Galindo  
**Proyecto:** No. 3  
**Dataset:** Bike Sharing — UCI

## Objetivo
Analizar y predecir la demanda mediante exploración, ETL, Data Mart, aprendizaje supervisado, análisis no supervisado y visualización en Power BI Desktop.

## Resultados
- 17,379 registros y 17 variables
- 0 faltantes y 0 duplicados completos
- Random Forest Regressor: R² ≈ 0.944
- Random Forest Classifier: Accuracy ≈ 0.877
- K-Means: k=4, Silhouette ≈ 0.178
- PCA: 2 componentes ≈ 43.90 % de varianza

## Ejecución
```powershell
.\.venv\Scripts\Activate.ps1
python src/etl.py
python src/modelos.py
python src/no_supervisado.py
python src/export_powerbi.py
```

## Dashboard final
Power BI Desktop. Archivo esperado:

```text
powerbi/Moya_MarkAlan_BikeSharing_Dashboard.pbix
```

## Storytelling
Problema -> datos -> preparación -> modelos -> patrones -> recomendaciones.
