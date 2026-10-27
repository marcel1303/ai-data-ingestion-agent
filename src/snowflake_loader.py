import os

import snowflake.connector
from dotenv import load_dotenv


def conectar_snowflake():
    load_dotenv()

    conexao = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        authenticator="snowflake",
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    return conexao


def inserir_registros(registros, nome_arquivo):
    if not registros:
        print("Nenhum registro para inserir.")
        return

    conexao = conectar_snowflake()
    cursor = None
    total_inseridos = 0

    try:
        cursor = conexao.cursor()

        comando_sql = """
            INSERT INTO RAW.SALES (
                CUSTOMER_ID,
                SALE_DATE,
                PRODUCT,
                QUANTITY,
                UNIT_PRICE,
                SOURCE_FILE,
                SOURCE_ROW_NUMBER
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        for numero_linha, registro in enumerate(registros, start=2):

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM RAW.SALES
                WHERE SOURCE_FILE = %s
                  AND SOURCE_ROW_NUMBER = %s
                """,
                (nome_arquivo, numero_linha)
            )

            quantidade_existente = cursor.fetchone()[0]

            if quantidade_existente > 0:
                print(f"Linha {numero_linha} já existe. Ignorando.")
                continue

            cursor.execute(
                comando_sql,
                (
                    registro["customer_id"],
                    registro["sale_date"],
                    registro["product"],
                    registro["quantity"],
                    registro["unit_price"],
                    nome_arquivo,
                    numero_linha
                )
            )

            total_inseridos += 1

        conexao.commit()

        print(f"{total_inseridos} registros inseridos com sucesso!")

    except Exception:
        conexao.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        conexao.close()