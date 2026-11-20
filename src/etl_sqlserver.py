from pathlib import Path
import pyodbc
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

SERVER = "localhost"
DATABASE = "BikeSharingDataMart"
DRIVER = "ODBC Driver 17 for SQL Server"

MASTER = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

DB = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


def crear_base():
    conn = pyodbc.connect(MASTER, autocommit=True)
    cur = conn.cursor()

    cur.execute("""
        IF DB_ID('BikeSharingDataMart') IS NULL
            CREATE DATABASE BikeSharingDataMart
    """)

    conn.close()


def crear_tablas(conn):
    cur = conn.cursor()

    cur.execute("""
    IF OBJECT_ID('dbo.dim_date', 'U') IS NULL
    CREATE TABLE dbo.dim_date (
        date_id INT PRIMARY KEY,
        fecha DATE NOT NULL,
        anio INT NOT NULL,
        trimestre INT NOT NULL,
        mes INT NOT NULL,
        nombre_mes VARCHAR(20) NOT NULL,
        dia INT NOT NULL,
        dia_semana INT NOT NULL,
        nombre_dia VARCHAR(20) NOT NULL,
        es_fin_semana BIT NOT NULL
    )
    """)

    cur.execute("""
    IF OBJECT_ID('dbo.dim_time', 'U') IS NULL
    CREATE TABLE dbo.dim_time (
        time_id INT PRIMARY KEY,
        hora INT NOT NULL,
        hora_texto VARCHAR(5) NOT NULL,
        periodo VARCHAR(20) NOT NULL
    )
    """)

    cur.execute("""
    IF OBJECT_ID('dbo.dim_weather', 'U') IS NULL
    CREATE TABLE dbo.dim_weather (
        weather_id INT PRIMARY KEY,
        weathersit INT NOT NULL,
        temp FLOAT NOT NULL,
        atemp FLOAT NOT NULL,
        hum FLOAT NOT NULL,
        windspeed FLOAT NOT NULL
    )
    """)

    cur.execute("""
    IF OBJECT_ID('dbo.fact_rentals', 'U') IS NULL
    CREATE TABLE dbo.fact_rentals (
        rental_id INT PRIMARY KEY,
        date_id INT NOT NULL,
        time_id INT NOT NULL,
        weather_id INT NOT NULL,
        casual INT NOT NULL,
        registered INT NOT NULL,
        cnt INT NOT NULL,

        CONSTRAINT FK_fact_date
            FOREIGN KEY(date_id)
            REFERENCES dbo.dim_date(date_id),

        CONSTRAINT FK_fact_time
            FOREIGN KEY(time_id)
            REFERENCES dbo.dim_time(time_id),

        CONSTRAINT FK_fact_weather
            FOREIGN KEY(weather_id)
            REFERENCES dbo.dim_weather(weather_id)
    )
    """)

    conn.commit()


def limpiar_tablas(conn):
    cur = conn.cursor()

    cur.execute("DELETE FROM dbo.fact_rentals")
    cur.execute("DELETE FROM dbo.dim_weather")
    cur.execute("DELETE FROM dbo.dim_time")
    cur.execute("DELETE FROM dbo.dim_date")

    conn.commit()


def cargar_dim_fecha(conn, df):
    inicio = pd.Timestamp(df["dteday"].min())
    fin = pd.Timestamp("2030-12-31")

    fechas = pd.date_range(
        inicio,
        fin,
        freq="D"
    )

    filas = []

    for fecha in fechas:
        date_id = int(fecha.strftime("%Y%m%d"))

        filas.append((
            date_id,
            fecha.date(),
            fecha.year,
            fecha.quarter,
            fecha.month,
            fecha.strftime("%B"),
            fecha.day,
            fecha.weekday() + 1,
            fecha.strftime("%A"),
            1 if fecha.weekday() >= 5 else 0
        ))

    cur = conn.cursor()
    cur.fast_executemany = True

    cur.executemany("""
        INSERT INTO dbo.dim_date
        (
            date_id,
            fecha,
            anio,
            trimestre,
            mes,
            nombre_mes,
            dia,
            dia_semana,
            nombre_dia,
            es_fin_semana
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, filas)

    conn.commit()


def cargar_dim_tiempo(conn):
    filas = []

    for hora in range(24):

        if hora <= 5:
            periodo = "Madrugada"
        elif hora <= 11:
            periodo = "Manana"
        elif hora <= 17:
            periodo = "Tarde"
        else:
            periodo = "Noche"

        filas.append((
            hora + 1,
            hora,
            f"{hora:02d}:00",
            periodo
        ))

    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO dbo.dim_time
        (
            time_id,
            hora,
            hora_texto,
            periodo
        )
        VALUES (?, ?, ?, ?)
    """, filas)

    conn.commit()


def cargar_dim_clima(conn, df):

    weather = (
        df[
            [
                "weathersit",
                "temp",
                "atemp",
                "hum",
                "windspeed"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    weather.insert(
        0,
        "weather_id",
        range(1, len(weather) + 1)
    )

    cur = conn.cursor()
    cur.fast_executemany = True

    filas = [
        (
            int(r.weather_id),
            int(r.weathersit),
            float(r.temp),
            float(r.atemp),
            float(r.hum),
            float(r.windspeed)
        )
        for r in weather.itertuples(index=False)
    ]

    cur.executemany("""
        INSERT INTO dbo.dim_weather
        (
            weather_id,
            weathersit,
            temp,
            atemp,
            hum,
            windspeed
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, filas)

    conn.commit()

    return weather


def cargar_hechos(conn, df, weather):

    weather_map = {}

    for r in weather.itertuples(index=False):

        llave = (
            r.weathersit,
            r.temp,
            r.atemp,
            r.hum,
            r.windspeed
        )

        weather_map[llave] = r.weather_id

    filas = []

    for r in df.itertuples(index=False):

        fecha = pd.Timestamp(r.dteday)

        date_id = int(fecha.strftime("%Y%m%d"))

        time_id = int(r.hr) + 1

        llave_clima = (
            r.weathersit,
            r.temp,
            r.atemp,
            r.hum,
            r.windspeed
        )

        weather_id = weather_map[llave_clima]

        filas.append((
            int(r.instant),
            date_id,
            time_id,
            int(weather_id),
            int(r.casual),
            int(r.registered),
            int(r.cnt)
        ))

    cur = conn.cursor()
    cur.fast_executemany = True

    cur.executemany("""
        INSERT INTO dbo.fact_rentals
        (
            rental_id,
            date_id,
            time_id,
            weather_id,
            casual,
            registered,
            cnt
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, filas)

    conn.commit()


def mostrar_conteos(conn):

    cur = conn.cursor()

    print("\n=== RESULTADO CARGA FULL ===")

    tablas = [
        "dim_date",
        "dim_time",
        "dim_weather",
        "fact_rentals"
    ]

    for tabla in tablas:

        cur.execute(
            f"SELECT COUNT(*) FROM dbo.{tabla}"
        )

        total = cur.fetchone()[0]

        print(f"{tabla}: {total:,}")


def main():

    print("=== BIKE SHARING - ETL FULL ===")

    df = pd.read_csv(
        RAW / "hour.csv"
    )

    df["dteday"] = pd.to_datetime(
        df["dteday"]
    )

    crear_base()

    conn = pyodbc.connect(DB)

    try:

        crear_tablas(conn)

        print("Borrando datos anteriores...")

        limpiar_tablas(conn)

        print("Cargando dimension fecha...")

        cargar_dim_fecha(
            conn,
            df
        )

        print("Cargando dimension tiempo...")

        cargar_dim_tiempo(conn)

        print("Cargando dimension clima...")

        weather = cargar_dim_clima(
            conn,
            df
        )

        print("Cargando tabla de hechos...")

        cargar_hechos(
            conn,
            df,
            weather
        )

        mostrar_conteos(conn)

        print(
            "\nCARGA FULL COMPLETADA CORRECTAMENTE"
        )

    finally:

        conn.close()


if __name__ == "__main__":
    main()
