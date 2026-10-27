# Revisión Unidad III - Modelos supervisados funcionando

## Regresión

| modelo                  |      MAE |    RMSE |       R2 |
|:------------------------|---------:|--------:|---------:|
| linear_regression       | 104.803  | 139.211 | 0.387981 |
| random_forest_regressor |  25.1212 |  42.169 | 0.943843 |

El objetivo es predecir `cnt`. Se excluyen `casual` y `registered` para evitar fuga de información.

## Clasificación

| modelo                   |   accuracy |   precision_macro |   recall_macro |   f1_macro |
|:-------------------------|-----------:|------------------:|---------------:|-----------:|
| logistic_regression      |   0.643268 |          0.638977 |       0.647975 |   0.639371 |
| random_forest_classifier |   0.877445 |          0.880068 |       0.878539 |   0.879206 |

Los niveles de demanda se definen con percentiles 33 y 67 calculados únicamente sobre el conjunto de entrenamiento: **69** y **228** rentas.

El mejor desempeño preliminar corresponde a Random Forest tanto para regresión como para clasificación.
