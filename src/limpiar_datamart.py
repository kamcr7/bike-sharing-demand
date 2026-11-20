import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=BikeSharingDataMart;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cur = conn.cursor()

print("=== LIMPIANDO DATA MART ===")

cur.execute("DELETE FROM dbo.fact_rentals")
cur.execute("DELETE FROM dbo.dim_weather")
cur.execute("DELETE FROM dbo.dim_time")
cur.execute("DELETE FROM dbo.dim_date")

conn.commit()

for tabla in [
    "fact_rentals",
    "dim_date",
    "dim_time",
    "dim_weather"
]:
    cur.execute(
        f"SELECT COUNT(*) FROM dbo.{tabla}"
    )

    total = cur.fetchone()[0]

    print(f"{tabla}: {total}")

conn.close()

print("DATA MART VACIO")
