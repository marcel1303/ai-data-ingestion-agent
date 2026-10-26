import os

import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    authenticator="snowflake",
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE"),
)

try:
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                CURRENT_DATABASE(),
                CURRENT_SCHEMA(),
                CURRENT_WAREHOUSE(),
                CURRENT_ROLE()
        """)

        resultado = cursor.fetchone()

        print("Conexão estabelecida com sucesso!")
        print("Banco:", resultado[0])
        print("Schema:", resultado[1])
        print("Warehouse:", resultado[2])
        print("Role:", resultado[3])

    finally:
        cursor.close()
finally:
    conn.close()
