from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_recall_fscore_support, confusion_matrix
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed' / 'bike_sharing_clean.csv'
OUT = ROOT / 'outputs'
MODELS = OUT / 'modelos'
METRICS = OUT / 'metricas'
PLOTS = OUT / 'graficas'
for p in (MODELS, METRICS, PLOTS):
    p.mkdir(parents=True, exist_ok=True)

FEATURES = ['hr','weekday','workingday','holiday','season','mnth','yr','weathersit','temp','atemp','hum','windspeed']


def regression(df):
    X = df[FEATURES]
    y = df['cnt']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    models = {
        'linear_regression': Pipeline([('scale', StandardScaler()), ('model', LinearRegression())]),
        'random_forest_regressor': RandomForestRegressor(n_estimators=80, max_depth=18, min_samples_leaf=2, random_state=42, n_jobs=-1)
    }
    rows=[]; best_name=None; best_r2=-1e9; best_model=None; best_pred=None
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        row={'modelo':name,'MAE':mean_absolute_error(y_test,pred),'RMSE':mean_squared_error(y_test,pred)**0.5,'R2':r2_score(y_test,pred)}
        rows.append(row)
        if row['R2'] > best_r2:
            best_r2=row['R2']; best_name=name; best_model=model; best_pred=pred
    pd.DataFrame(rows).to_csv(METRICS/'regresion_metricas.csv',index=False)
    joblib.dump(best_model,MODELS/'mejor_modelo_regresion.joblib')
    plt.figure(figsize=(7,5)); plt.scatter(y_test,best_pred,s=8,alpha=0.35)
    mn=min(y_test.min(),best_pred.min()); mx=max(y_test.max(),best_pred.max()); plt.plot([mn,mx],[mn,mx],linewidth=1)
    plt.xlabel('cnt real'); plt.ylabel('cnt predicho'); plt.title(f'Regresión - {best_name}'); plt.tight_layout()
    plt.savefig(PLOTS/'regresion_real_vs_predicho.png',dpi=150); plt.close()
    return rows,best_name


def classify_levels(y,q33,q67):
    return pd.cut(y,bins=[-np.inf,q33,q67,np.inf],labels=['baja','media','alta'],include_lowest=True)


def classification(df):
    X=df[FEATURES]; y_cnt=df['cnt']
    X_train,X_test,y_train_cnt,y_test_cnt=train_test_split(X,y_cnt,test_size=0.2,random_state=42)
    q33,q67=y_train_cnt.quantile([0.33,0.67]).tolist()
    y_train=classify_levels(y_train_cnt,q33,q67); y_test=classify_levels(y_test_cnt,q33,q67)
    models={
        'logistic_regression':Pipeline([('scale',StandardScaler()),('model',LogisticRegression(max_iter=800))]),
        'random_forest_classifier':RandomForestClassifier(n_estimators=80,max_depth=18,min_samples_leaf=2,random_state=42,n_jobs=-1)
    }
    rows=[]; best_name=None; best_f1=-1; best_model=None; best_pred=None
    for name,model in models.items():
        model.fit(X_train,y_train); pred=model.predict(X_test)
        precision,recall,f1,_=precision_recall_fscore_support(y_test,pred,average='macro',zero_division=0)
        row={'modelo':name,'accuracy':accuracy_score(y_test,pred),'precision_macro':precision,'recall_macro':recall,'f1_macro':f1}
        rows.append(row)
        if f1>best_f1:
            best_f1=f1; best_name=name; best_model=model; best_pred=pred
    pd.DataFrame(rows).to_csv(METRICS/'clasificacion_metricas.csv',index=False)
    with open(METRICS/'clasificacion_umbral.json','w',encoding='utf-8') as f: json.dump({'percentil_33':q33,'percentil_67':q67},f,indent=2)
    joblib.dump(best_model,MODELS/'mejor_modelo_clasificacion.joblib')
    labels=['baja','media','alta']; cm=confusion_matrix(y_test,best_pred,labels=labels)
    pd.DataFrame(cm,index=labels,columns=labels).to_csv(METRICS/'matriz_confusion_clasificacion.csv')
    plt.figure(figsize=(5,4)); plt.imshow(cm,interpolation='nearest'); plt.title(f'Matriz de confusión - {best_name}'); plt.colorbar()
    plt.xticks(range(3),labels); plt.yticks(range(3),labels); plt.xlabel('Predicción'); plt.ylabel('Real')
    for i in range(3):
        for j in range(3): plt.text(j,i,str(cm[i,j]),ha='center',va='center')
    plt.tight_layout(); plt.savefig(PLOTS/'clasificacion_matriz_confusion.png',dpi=150); plt.close()
    return rows,best_name,q33,q67


def main():
    df=pd.read_csv(DATA)
    reg_rows,reg_best=regression(df)
    cls_rows,cls_best,q33,q67=classification(df)
    summary={'features':FEATURES,'nota_fuga_datos':'casual y registered se excluyen porque cnt = casual + registered','regresion_mejor_modelo':reg_best,'clasificacion_mejor_modelo':cls_best,'clasificacion_percentil_33':q33,'clasificacion_percentil_67':q67}
    with open(METRICS/'resumen_modelos.json','w',encoding='utf-8') as f: json.dump(summary,f,indent=2,ensure_ascii=False)
    print('Modelos ejecutados correctamente')
    print(pd.DataFrame(reg_rows).to_string(index=False))
    print(pd.DataFrame(cls_rows).to_string(index=False))
    print('Umbrales:',q33,q67)

if __name__=='__main__':
    main()
