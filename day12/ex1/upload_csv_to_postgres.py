import pandas as pd
import psycopg2

# === Configuration ===
CSV_FILE = "people.csv"
DB_CONFIG = {
    "dbname": "user_db",
    "user": "khoitm",
    "password": "123456",
    "host": "localhost",
    "port": "5432",
}
TABLE_NAME = "user"

# === Read CSV ===
df = pd.read_csv(CSV_FILE)

# === Normalize Column Names ===
df.columns = [col.strip().lower() for col in df.columns]  # Standardize to lowercase, remove extra spaces

# === Connect to PostgreSQL ===
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# === Optional: Create table if not exists (basic version) ===
columns = ", ".join([f"{col} TEXT" for col in df.columns])
cur.execute(f"""
    CREATE TABLE IF NOT EXISTS "{TABLE_NAME}" (
        {columns}
    );
""")

# === Insert rows ===
for _, row in df.iterrows():
    # Create placeholders for each row
    placeholders = ', '.join(['%s'] * len(row))
    
    # Specify the column names explicitly to avoid order issues
    column_names = ', '.join([f'"{col}"' for col in df.columns])
    
    # Construct SQL query with column names and placeholders
    sql = f'INSERT INTO "{TABLE_NAME}" ({column_names}) VALUES ({placeholders})'
    
    # Execute the query
    cur.execute(sql, tuple(row))

conn.commit()
cur.close()
conn.close()

print(f"Uploaded {len(df)} rows to table '{TABLE_NAME}'.")
