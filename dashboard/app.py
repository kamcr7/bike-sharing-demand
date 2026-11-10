from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Bike Sharing - Diagnostico U2",
    page_icon="🚲",
    layout="wide",
)

st.markdown("""
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {
    background: #f7f8fb;
    border: 1px solid #e2e5ea;
    padding: 14px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "hour.csv"

@st.cache_data
def cargar_datos(path):
    return pd.read_csv(path)

if not DATA_PATH.exists():
    st.error(f"No se encontro el dataset original: {DATA_PATH}")
    st.stop()

df = cargar_datos(DATA_PATH)

SEASONS = {1:"Primavera",2:"Verano",3:"Otono",4:"Invierno"}
WEATHER = {
    1:"Despejado / pocas nubes",
    2:"Niebla / nublado",
    3:"Lluvia o nieve ligera",
    4:"Condiciones severas"
}

st.title("🚲 Bike Sharing - Exploracion y diagnostico")
st.caption("Unidad II · Actividad de Evaluacion 1 · Mark Alan Moya Galindo")
st.info("El dashboard lee directamente `data/raw/hour.csv`. No limpia, elimina ni modifica el dataset original.")

with st.sidebar:
    st.header("Filtros")
    year = st.selectbox("Anio", ["Todos", 2011, 2012])
    season = st.selectbox("Temporada", ["Todas",1,2,3,4],
                          format_func=lambda x: "Todas" if x=="Todas" else SEASONS[x])
    weather = st.selectbox("Clima", ["Todos",1,2,3,4],
                           format_func=lambda x: "Todos" if x=="Todos" else WEATHER[x])
    hour_range = st.slider("Rango de hora", 0, 23, (0,23))
    workday = st.selectbox("Tipo de dia", ["Todos","Laborable","No laborable"])

view = df.copy()
if year == 2011:
    view = view[view["yr"] == 0]
elif year == 2012:
    view = view[view["yr"] == 1]
if season != "Todas":
    view = view[view["season"] == season]
if weather != "Todos":
    view = view[view["weathersit"] == weather]
view = view[view["hr"].between(hour_range[0], hour_range[1])]
if workday == "Laborable":
    view = view[view["workingday"] == 1]
elif workday == "No laborable":
    view = view[view["workingday"] == 0]

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Registros", f"{len(df):,}")
c2.metric("Variables", df.shape[1])
c3.metric("Faltantes", int(df.isnull().sum().sum()))
c4.metric("Duplicados", int(df.duplicated().sum()))
c5.metric("Demanda promedio", f"{df['cnt'].mean():.1f}")

tabs = st.tabs(["Datos","Calidad","Estadistica","Visualizaciones","Analisis posterior"])

with tabs[0]:
    st.subheader("Datos originales")
    st.write(f"Registros despues de filtros: **{len(view):,}**")
    st.dataframe(view.head(250), use_container_width=True, height=430)

    st.subheader("Estructura")
    left, right = st.columns(2)
    with left:
        st.write("**Columnas**")
        st.code("\n".join(df.columns))
    with right:
        tipos = pd.DataFrame({"Variable":df.columns,"Tipo":[str(x) for x in df.dtypes]})
        st.write("**Tipos de datos**")
        st.dataframe(tipos, use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader("Valores faltantes")
    faltantes = df.isnull().sum().to_frame("Faltantes")
    faltantes["Porcentaje"] = (faltantes["Faltantes"]/len(df)*100).round(2)
    st.dataframe(faltantes, use_container_width=True)

    st.subheader("Registros duplicados")
    st.metric("Filas completas duplicadas", int(df.duplicated().sum()))

    st.subheader("Comprobaciones de consistencia")
    checks = {
        "season entre 1 y 4": df["season"].between(1,4).all(),
        "yr entre 0 y 1": df["yr"].between(0,1).all(),
        "mnth entre 1 y 12": df["mnth"].between(1,12).all(),
        "hr entre 0 y 23": df["hr"].between(0,23).all(),
        "weekday entre 0 y 6": df["weekday"].between(0,6).all(),
        "weathersit entre 1 y 4": df["weathersit"].between(1,4).all(),
        "temp, atemp, hum, windspeed entre 0 y 1":
            df[["temp","atemp","hum","windspeed"]].ge(0).all().all()
            and df[["temp","atemp","hum","windspeed"]].le(1).all().all(),
        "conteos no negativos": df[["casual","registered","cnt"]].ge(0).all().all(),
        "cnt = casual + registered": (df["cnt"] == df["casual"] + df["registered"]).all(),
    }
    st.dataframe(pd.DataFrame({"Comprobacion":checks.keys(),"Cumple":checks.values()}),
                 use_container_width=True, hide_index=True)

    st.subheader("Posibles valores atipicos por IQR")
    rows=[]
    for col in ["cnt","temp","hum","windspeed"]:
        q1,q3=df[col].quantile(.25),df[col].quantile(.75)
        iqr=q3-q1
        li,ls=q1-1.5*iqr,q3+1.5*iqr
        n=int(((df[col]<li)|(df[col]>ls)).sum())
        rows.append([col,q1,q3,li,ls,n])
    st.dataframe(pd.DataFrame(rows,columns=[
        "Variable","Q1","Q3","Limite inferior","Limite superior","Posibles atipicos"
    ]).round(4), use_container_width=True, hide_index=True)
    st.warning("Un valor atipico no es automaticamente un error. En esta actividad solo se diagnostica.")

with tabs[2]:
    st.subheader("Estadistica descriptiva inicial")
    variables=["cnt","temp","hum"]
    stats=pd.DataFrame({
        "Media":df[variables].mean(),
        "Mediana":df[variables].median(),
        "Minimo":df[variables].min(),
        "Maximo":df[variables].max(),
        "Desviacion estandar":df[variables].std()
    })
    st.dataframe(stats.round(4), use_container_width=True)
    st.write(
        f"La demanda (`cnt`) tiene media **{df['cnt'].mean():.2f}**, mediana **{df['cnt'].median():.0f}** "
        f"y desviacion estandar **{df['cnt'].std():.2f}**, mostrando una variacion alta entre horas."
    )

with tabs[3]:
    st.subheader("Demanda promedio por hora")
    by_hour=view.groupby("hr")["cnt"].mean()
    fig,ax=plt.subplots(figsize=(10,4))
    ax.plot(by_hour.index,by_hour.values,marker="o")
    ax.set_xlabel("Hora")
    ax.set_ylabel("Promedio de rentas")
    ax.grid(alpha=.3)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    a,b=st.columns(2)
    with a:
        st.subheader("Demanda por clima")
        by_weather=view.groupby("weathersit")["cnt"].mean()
        fig,ax=plt.subplots(figsize=(6,4))
        ax.bar(by_weather.index.astype(str),by_weather.values)
        ax.set_xlabel("weathersit")
        ax.set_ylabel("Promedio de rentas")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with b:
        st.subheader("Demanda por temporada")
        by_season=view.groupby("season")["cnt"].mean()
        fig,ax=plt.subplots(figsize=(6,4))
        ax.bar([SEASONS[x] for x in by_season.index],by_season.values)
        ax.tick_params(axis="x",rotation=20)
        ax.set_ylabel("Promedio de rentas")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    a,b=st.columns(2)
    with a:
        st.subheader("Distribucion de cnt")
        fig,ax=plt.subplots(figsize=(6,4))
        ax.hist(view["cnt"],bins=30,edgecolor="black",linewidth=.4)
        ax.set_xlabel("Rentas por hora")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with b:
        st.subheader("Temperatura vs demanda")
        muestra=view.sample(min(2500,len(view)),random_state=42) if len(view) else view
        fig,ax=plt.subplots(figsize=(6,4))
        ax.scatter(muestra["temp"],muestra["cnt"],alpha=.25,s=12)
        ax.set_xlabel("Temperatura normalizada")
        ax.set_ylabel("cnt")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.subheader("Boxplots")
    fig,axes=plt.subplots(1,3,figsize=(11,4))
    for ax,col in zip(axes,["cnt","hum","windspeed"]):
        ax.boxplot(df[col].dropna())
        ax.set_title(col)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with tabs[4]:
    st.subheader("Regresion")
    st.markdown("""
- Objetivo: `cnt`.
- Entradas propuestas: `hr`, `weekday`, `workingday`, `holiday`, `season`, `mnth`, `yr`, `weathersit`, `temp`, `atemp`, `hum`, `windspeed`.
- `casual` y `registered` no se usan como predictores directos porque su suma produce `cnt`.
""")
    st.subheader("Clasificacion")
    st.markdown("""
- Objetivo propuesto: nivel de demanda.
- Clases: baja, media y alta.
- Los cortes se documentaran antes del modelado con un criterio reproducible.
""")
    st.subheader("Agrupamiento")
    st.markdown("""
- Variables sugeridas: `hr`, `weekday`, `season`, `weathersit`, `temp`, `hum`, `windspeed`, `cnt`.
- Objetivo: identificar perfiles de uso por horario, clima, temporada y volumen de demanda.
""")
    st.success("Diagnostico: los datos son adecuados para continuar con las siguientes etapas del proyecto.")
