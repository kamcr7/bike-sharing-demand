-- Data Mart Bike Sharing
-- Proyecto Integrador de Recursamiento ECBD 2026
-- Alumno: Mark Alan Moya Galindo
-- Compatible con SQLite y alineado con src/etl.py.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fact_rentals;
DROP TABLE IF EXISTS dim_weather;
DROP TABLE IF EXISTS dim_time;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    dteday TEXT NOT NULL,
    yr INTEGER NOT NULL,
    mnth INTEGER NOT NULL,
    weekday INTEGER NOT NULL,
    workingday INTEGER NOT NULL,
    holiday INTEGER NOT NULL,
    season INTEGER NOT NULL,
    year_full INTEGER,
    month_name TEXT,
    day_name TEXT,
    is_weekend INTEGER
);

CREATE TABLE dim_time (
    time_id INTEGER PRIMARY KEY,
    hr INTEGER NOT NULL UNIQUE,
    time_period TEXT
);

CREATE TABLE dim_weather (
    weather_id INTEGER PRIMARY KEY,
    weathersit INTEGER NOT NULL,
    temp REAL NOT NULL,
    atemp REAL NOT NULL,
    hum REAL NOT NULL,
    windspeed REAL NOT NULL,
    temp_c REAL,
    atemp_c REAL,
    humidity_pct REAL,
    windspeed_real REAL
);

CREATE TABLE fact_rentals (
    rental_id INTEGER PRIMARY KEY,
    date_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    weather_id INTEGER NOT NULL,
    casual INTEGER NOT NULL,
    registered INTEGER NOT NULL,
    cnt INTEGER NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
    FOREIGN KEY (weather_id) REFERENCES dim_weather(weather_id)
);

CREATE INDEX idx_fact_date ON fact_rentals(date_id);
CREATE INDEX idx_fact_time ON fact_rentals(time_id);
CREATE INDEX idx_fact_weather ON fact_rentals(weather_id);

-- Consultas de verificacion sugeridas:
-- SELECT COUNT(*) FROM fact_rentals;
--
-- SELECT t.hr, AVG(f.cnt) AS demanda_promedio
-- FROM fact_rentals f
-- JOIN dim_time t ON f.time_id = t.time_id
-- GROUP BY t.hr
-- ORDER BY t.hr;
--
-- SELECT w.weathersit, AVG(f.cnt) AS demanda_promedio
-- FROM fact_rentals f
-- JOIN dim_weather w ON f.weather_id = w.weather_id
-- GROUP BY w.weathersit
-- ORDER BY w.weathersit;
