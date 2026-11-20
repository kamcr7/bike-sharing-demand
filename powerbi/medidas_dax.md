# Medidas DAX

```DAX
Total Rentas = SUM(fact_rentals[cnt])
```

```DAX
Promedio Demanda = AVERAGE(fact_rentals[cnt])
```

```DAX
Max Demanda = MAX(fact_rentals[cnt])
```

```DAX
Total Registros = COUNTROWS(fact_rentals)
```

```DAX
Usuarios Casuales = SUM(fact_rentals[casual])
```

```DAX
Usuarios Registrados = SUM(fact_rentals[registered])
```

```DAX
Porcentaje Registrados = DIVIDE([Usuarios Registrados], [Total Rentas], 0)
```

Resultados de referencia:
- Random Forest Regressor: R² ≈ 0.943843, MAE ≈ 25.121, RMSE ≈ 42.169.
- Random Forest Classifier: Accuracy ≈ 0.877445, F1 ≈ 0.879206.
- K-Means: k = 4, Silhouette ≈ 0.177637.
- PCA: PC1 ≈ 25.28 %, PC2 ≈ 18.62 %, total ≈ 43.90 %.
