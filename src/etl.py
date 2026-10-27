from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
OUTPUTS = ROOT / 'outputs'
PROCESSED.mkdir(parents=True, exist_ok=True)
OUTPUTS.mkdir(parents=True, exist_ok=True)


def load_data():
    hour = pd.read_csv(RAW / 'hour.csv')
    day = pd.read_csv(RAW / 'day.csv')
    return hour, day


def validate(df: pd.DataFrame, name: str):
    return {
        'dataset': name,
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': int(df.isna().sum().sum()),
        'duplicate_rows': int(df.duplicated().sum()),
    }


def transform_hour(hour: pd.DataFrame) -> pd.DataFrame:
    df = hour.copy()
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year_full'] = df['dteday'].dt.year
    df['month_name'] = df['dteday'].dt.month_name()
    df['day_name'] = df['dteday'].dt.day_name()
    df['is_weekend'] = (df['weekday'].isin([0, 6])).astype(int)
    df['temp_c'] = (df['temp'] * 41).round(2)
    df['atemp_c'] = (df['atemp'] * 50).round(2)
    df['humidity_pct'] = (df['hum'] * 100).round(2)
    df['windspeed_real'] = (df['windspeed'] * 67).round(2)
    df['dteday'] = df['dteday'].dt.strftime('%Y-%m-%d')
    return df


def create_datamart(df: pd.DataFrame, db_path: Path):
    conn = sqlite3.connect(db_path)
    try:
        dim_date = (df[['dteday','yr','mnth','weekday','workingday','holiday','season','year_full','month_name','day_name','is_weekend']]
                    .drop_duplicates().reset_index(drop=True))
        dim_date.insert(0, 'date_id', range(1, len(dim_date)+1))

        dim_time = pd.DataFrame({'hr': sorted(df['hr'].unique())})
        dim_time.insert(0, 'time_id', range(1, len(dim_time)+1))
        dim_time['time_period'] = pd.cut(dim_time['hr'], bins=[-1,5,11,17,23], labels=['Madrugada','Mañana','Tarde','Noche'])

        dim_weather = (df[['weathersit','temp','atemp','hum','windspeed','temp_c','atemp_c','humidity_pct','windspeed_real']]
                       .drop_duplicates().reset_index(drop=True))
        dim_weather.insert(0, 'weather_id', range(1, len(dim_weather)+1))

        fact = df[['instant','dteday','hr','weathersit','temp','atemp','hum','windspeed','casual','registered','cnt']].copy()
        fact = fact.merge(dim_date[['date_id','dteday']], on='dteday', how='left')
        fact = fact.merge(dim_time[['time_id','hr']], on='hr', how='left')
        fact = fact.merge(dim_weather[['weather_id','weathersit','temp','atemp','hum','windspeed']],
                          on=['weathersit','temp','atemp','hum','windspeed'], how='left')
        fact = fact[['instant','date_id','time_id','weather_id','casual','registered','cnt']]
        fact = fact.rename(columns={'instant':'rental_id'})

        dim_date.to_sql('dim_date', conn, if_exists='replace', index=False)
        dim_time.to_sql('dim_time', conn, if_exists='replace', index=False)
        dim_weather.to_sql('dim_weather', conn, if_exists='replace', index=False)
        fact.to_sql('fact_rentals', conn, if_exists='replace', index=False)
    finally:
        conn.close()


def main():
    hour, day = load_data()
    validation = pd.DataFrame([validate(hour, 'hour.csv'), validate(day, 'day.csv')])
    validation.to_csv(OUTPUTS / 'validacion_datos.csv', index=False)

    processed = transform_hour(hour)
    processed.to_csv(PROCESSED / 'bike_sharing_clean.csv', index=False)

    create_datamart(processed, PROCESSED / 'bike_sharing_datamart.db')

    print('ETL completado')
    print(validation.to_string(index=False))
    print(f'Dataset procesado: {PROCESSED / "bike_sharing_clean.csv"}')
    print(f'Data Mart SQLite: {PROCESSED / "bike_sharing_datamart.db"}')

if __name__ == '__main__':
    main()
