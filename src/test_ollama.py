import requests
import json
import sys

from validators import validar_mapeamento
from csv_reader import extrair_colunas_csv, ler_registros_csv
from transformer import aplicar_mapeamento
from snowflake_loader import inserir_registros

# Endereço da API local do Ollama
url = "http://localhost:11434/api/generate"

# Dados enviados ao modelo
payload = {
    "model": "qwen3:4b",
    
"prompt": """
Você é um assistente de engenharia de dados.

Sua tarefa é mapear colunas de um arquivo CSV
para um schema de destino.

Colunas de origem:
ID_CLIENTE, DT, ITEM, QTD, PRECO_UN.

Colunas de destino:
customer_id, sale_date, product, quantity, unit_price.

REGRAS OBRIGATÓRIAS:

1. As CHAVES do JSON devem ser exclusivamente
   os nomes das colunas de ORIGEM.

2. Os VALORES do JSON devem ser exclusivamente
   os nomes das colunas de DESTINO.

3. Não inverta a direção do mapeamento.

4. Não invente colunas.

5. Responda exclusivamente com um objeto JSON.

Exemplo de formato esperado:
{
    "ID_CLIENTE": "customer_id",
    "DT": "sale_date"
}
""",

    "format": "json",
    "stream": False
}

# Envia a requisição para o Ollama
response = requests.post(url, json=payload)
response.raise_for_status()

# Converte a resposta HTTP em um dicionário Python
resultado = response.json()

# Exibe a resposta gerada pelo modelo
print(resultado["response"])

# Colunas que realmente existem na origem
colunas_origem = extrair_colunas_csv("data/raw/vendas.csv")

colunas_destino = [
    "customer_id",
    "sale_date",
    "product",
    "quantity",
    "unit_price"
]

# Converte o JSON gerado pela IA em um dicionário
mapeamento = json.loads(resultado["response"])

# Executa a validação completa do mapeamento
erros = validar_mapeamento(
    mapeamento,
    colunas_origem,
    colunas_destino
)

# Apresenta o resultado da validação
if not erros:
    print("\nSTATUS FINAL: APROVADO")
    print("Mapeamento liberado para a próxima etapa.")

    registros = ler_registros_csv("data/raw/vendas.csv")

    registros_transformados = aplicar_mapeamento(
        registros,
        mapeamento
    )

    print("\nREGISTROS TRANSFORMADOS:")

    for registro in registros_transformados:
        print(registro)

    # Ingestão executada somente após aprovação
    print("\nINICIANDO INGESTÃO NO SNOWFLAKE...")

    inserir_registros(
        registros=registros_transformados,
        nome_arquivo="vendas.csv"
    )

else:
    for erro in erros:
        print(f"ERRO: {erro}")

    print("\nSTATUS FINAL: REPROVADO")
    print("Mapeamento bloqueado para revisão.")
    sys.exit(1)