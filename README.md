
# AI Data Ingestion Agent

### POC de ingestão de dados assistida por Inteligência Artificial

## 1. Visão geral

Este projeto é uma Prova de Conceito (POC) voltada à aplicação
de Inteligência Artificial em processos de engenharia de dados.

O objetivo é explorar como modelos de linguagem (LLMs)
podem auxiliar na identificação e no mapeamento de colunas
entre diferentes estruturas de dados, reduzindo o esforço
manual necessário para integrar novas fontes.

A solução utiliza Python e um modelo de linguagem executado
localmente por meio do Ollama.

Nesta primeira etapa, foi desenvolvido um componente funcional
que permite:

- Solicitar a um LLM sugestões de mapeamento entre colunas
  de origem e destino.
- Receber o mapeamento em formato JSON.
- Validar o resultado utilizando regras determinísticas.
- Identificar inconsistências antes que o mapeamento
  seja utilizado nas próximas etapas do processamento.
- Executar testes automatizados com pytest.

**Status atual:** primeira etapa funcional da POC,
contemplando sugestão e validação de mapeamentos de schema.

A ingestão efetiva de arquivos, o armazenamento e as
transformações de dados serão implementados nas próximas fases.


## 2. Arquitetura técnica

A arquitetura atual da POC é composta por três elementos:

**1. Python**

Responsável por definir os schemas de origem e destino,
enviar requisições ao modelo de linguagem e controlar
o fluxo de execução.

**2. Ollama + Qwen3:4b**

O Ollama disponibiliza uma API local para execução do LLM.

O modelo Qwen3:4b recebe os nomes das colunas e sugere
as correspondências entre os schemas, retornando um JSON.

**3. Validação determinística**

O módulo `validators.py` verifica se o mapeamento
gerado atende às regras estabelecidas.

As validações implementadas incluem:

- Existência das colunas de origem.
- Existência das colunas de destino.
- Identificação de destinos duplicados.
- Identificação de colunas de origem não mapeadas.

Quando o mapeamento apresenta inconsistências, o processo
é reprovado e sua execução é interrompida.

### Fluxo de processamento

1. O Python define as colunas de origem e destino.
2. O prompt é enviado ao Qwen por meio da API do Ollama.
3. O modelo retorna uma sugestão de mapeamento em JSON.
4. O Python converte a resposta em um dicionário.
5. O módulo de validação verifica as regras estabelecidas.
6. O processo retorna o status APROVADO ou REPROVADO.

A decisão de aprovação não é delegada ao LLM.
Ela é determinada pelas regras implementadas em Python.


## 3. Exemplo de funcionamento

Nesta primeira etapa, a POC utiliza schemas definidos
diretamente no código Python.

### Schema de origem

```text
ID_CLIENTE, DT, ITEM, QTD, PRECO_UN
```

### Schema de destino

```text
customer_id, sale_date, product, quantity, unit_price
```

### Mapeamento sugerido pelo LLM

```json
{
    "ID_CLIENTE": "customer_id",
    "DT": "sale_date",
    "ITEM": "product",
    "QTD": "quantity",
    "PRECO_UN": "unit_price"
}
```

### Cenário 1 — Mapeamento aprovado

Quando todas as correspondências atendem às regras
de validação, o processo apresenta:

```text
STATUS FINAL: APROVADO
Mapeamento liberado para a próxima etapa.
```

O processo termina com código de saída `0`.

### Cenário 2 — Mapeamento reprovado

Durante os testes, simulamos uma correspondência inválida:

```text
ID_CLIENTE → customer_name
```

Como `customer_name` não existe no schema de destino,
a validação identifica a inconsistência:

```text
ERRO: Destino inexistente: 'customer_name'

STATUS FINAL: REPROVADO
Mapeamento bloqueado para revisão.
```

Nesse cenário, o script utiliza `sys.exit(1)` para
sinalizar a falha e interromper sua execução.

**Observação:** os schemas ainda são definidos no código.
A leitura e a ingestão efetiva de arquivos CSV serão
implementadas em etapas futuras.


## 4. Testes automatizados

O projeto utiliza `pytest` para verificar o comportamento
das funções de validação.

Atualmente, foram implementados seis testes:

| Teste | Objetivo |
|---|---|
| `test_validar_coluna_origem` | Verificar a existência de colunas de origem |
| `test_validar_coluna_destino` | Verificar a existência de colunas de destino |
| `test_validar_destino_duplicado` | Identificar destinos já utilizados |
| `test_identificar_colunas_nao_mapeadas` | Identificar colunas de origem sem correspondência |
| `test_validar_mapeamento_completo` | Aprovar um mapeamento estruturalmente válido |
| `test_validar_mapeamento_invalido` | Identificar um destino inexistente |

### Executando os testes

Na raiz do projeto, com o ambiente virtual ativo:

```powershell
python -m pytest tests/test_validators.py -v
```

Resultado obtido durante o desenvolvimento:

```text
collected 6 items

test_validar_coluna_origem PASSED
test_validar_coluna_destino PASSED
test_validar_destino_duplicado PASSED
test_identificar_colunas_nao_mapeadas PASSED
test_validar_mapeamento_completo PASSED
test_validar_mapeamento_invalido PASSED
```

Os testes verificam regras específicas e cenários
de aprovação e reprovação.

A aprovação dos seis testes não representa cobertura
completa do código nem garante que todas as sugestões
do LLM sejam semanticamente corretas.


## 5. Como executar o projeto

### Pré-requisitos

Para reproduzir o ambiente de desenvolvimento, são necessários:

- Python 3.11 (versão utilizada: 3.11.7).
- Git.
- Ollama instalado e em execução.
- Modelo `qwen3:4b` disponível localmente.


### 5.1. Clonar o repositório

Após a publicação no GitHub, clone o projeto utilizando
a URL disponibilizada na página do repositório:

```powershell
git clone URL_DO_REPOSITORIO
cd ai-data-ingestion-agent
```

Substitua `URL_DO_REPOSITORIO` pelo endereço real
do repositório.

### 5.2. Criar o ambiente virtual

No Windows, utilizando PowerShell:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5.3. Instalar as dependências Python

```powershell
python -m pip install -r requirements.txt
```

### 5.4. Preparar o modelo de linguagem

Com o Ollama instalado, baixe o modelo utilizado na POC:

```powershell
ollama pull qwen3:4b
```

Certifique-se de que o servidor local do Ollama
esteja em execução.

A aplicação utiliza o endpoint:

`http://localhost:11434/api/generate`

### 5.5. Executar o mapeamento assistido por IA

Na raiz do projeto:

```powershell
python src/test_ollama.py
```

O script envia os schemas ao Qwen, recebe o mapeamento
em JSON e executa as regras de validação.

Quando o resultado atende às regras estabelecidas,
o processo apresenta:

```text
STATUS FINAL: APROVADO
Mapeamento liberado para a próxima etapa.
```

### 5.6. Executar os testes automatizados

```powershell
python -m pytest tests/test_validators.py -v
```

Os testes podem ser executados sem consultar o Ollama,
pois verificam diretamente as funções de validação.


## 6. Roadmap de evolução

O desenvolvimento da POC está organizado em etapas
incrementais, priorizando aprendizado prático,
testabilidade e qualidade dos dados.

### Etapa 1 — Mapeamento de schemas assistido por IA

**Status: Implementado**

- [x] Integração com Ollama e Qwen3:4b.
- [x] Geração de sugestões de mapeamento em JSON.
- [x] Validação de colunas de origem e destino.
- [x] Identificação de destinos duplicados.
- [x] Identificação de colunas não mapeadas.
- [x] Testes automatizados com pytest.

### Etapa 2 — Ingestão de arquivos CSV

**Status: Planejado**

- [ ] Leitura de arquivos CSV reais.
- [ ] Extração automática das colunas de origem.
- [ ] Validação de tipos de dados.
- [ ] Aplicação dos mapeamentos aprovados.
- [ ] Tratamento de inconsistências nos registros.

### Etapa 3 — Armazenamento com AWS S3

**Status: Planejado**

- [ ] Configuração do armazenamento.
- [ ] Organização dos arquivos de origem.
- [ ] Persistência dos arquivos processados.
- [ ] Definição de estratégias de rastreabilidade.

### Etapa 4 — Integração com Snowflake

**Status: Planejado**

- [ ] Configuração do ambiente analítico.
- [ ] Criação das estruturas de destino.
- [ ] Carga dos dados validados.
- [ ] Verificação de integridade após a carga.

### Etapa 5 — Transformações com dbt

**Status: Planejado**

- [ ] Criação dos modelos de transformação.
- [ ] Padronização dos dados.
- [ ] Implementação de testes de qualidade.
- [ ] Documentação dos modelos analíticos.

### Etapa 6 — Visualização e observabilidade

**Status: Planejado**

- [ ] Criação de um dashboard analítico.
- [ ] Acompanhamento das execuções.
- [ ] Monitoramento de erros e rejeições.
- [ ] Análise da qualidade dos dados processados.

## 7. Limitações atuais

Esta versão representa a primeira etapa funcional
de uma POC de ingestão assistida por IA.

As principais limitações são:

- Os schemas são definidos diretamente no código.
- Ainda não existe ingestão efetiva de arquivos CSV.
- As validações atuais verificam a integridade estrutural,
  mas não garantem a correção semântica do mapeamento.
- Ainda não há validação dos tipos de dados dos registros.
- O fluxo depende da disponibilidade local do Ollama.
- Ainda não existe integração com S3, Snowflake ou dbt.
- O projeto ainda não implementa um agente autônomo.
- A resposta do LLM ainda não possui tratamento específico
  para falhas de conexão, timeout ou JSON inválido.

As próximas etapas buscarão evoluir a solução
de forma incremental, mantendo a separação entre
sugestões produzidas pelo LLM e validações
determinísticas de qualidade.