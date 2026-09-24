# Incident Agent

Agente experimental para classificação e tratamento automatizado de incidentes utilizando **LangGraph**, **LangChain** e um modelo de linguagem executado localmente através do **Ollama**.

O agente recebe um incidente, classifica a área responsável (`DB` ou `OPS`), executa a ferramenta correspondente e valida o resultado da execução.

> **Status:** Experimental / Proof of Concept

---

## Architecture

```text
                         ┌──────────────┐
                         │   Incident   │
                         └──────┬───────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    Classifier   │
                       │     Qwen 3      │
                       └────────┬────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
              ┌───────────┐           ┌───────────┐
              │     DB    │           │    OPS    │
              │    Tool   │           │    Tool   │
              └─────┬─────┘           └─────┬─────┘
                    │                       │
                    └───────────┬───────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    Validator    │
                       │     Qwen 3      │
                       └────────┬────────┘
                                │
                         ┌──────┴──────┐
                         │             │
                      Success        Failure
                         │             │
                         ▼             ▼
                        END          Retry
                                       │
                                       ▼
                                  Classifier
```

---

## Features

- **Classificação automática** de incidentes.
- **Roteamento** para áreas `DB` e `OPS`.
- **Tools específicas** para cada área.
- **Validação** do resultado da execução.
- **Retry controlado** pelo LangGraph.
- **Estado compartilhado** entre os nodes.
- **Modelo de linguagem** executado localmente.
- Nenhuma API paga necessária.

---

## Tech Stack

| Tecnologia | Versão |
| :--- | :--- |
| **Python** | 3.11.9 |
| **LangGraph** | 1.2.12 |
| **LangChain** | 1.4.2 |
| **LangChain Core** | 1.6.4 |
| **LangChain Ollama** | 1.1.0 |
| **Pydantic** | 2.13.5 |
| **Python Dotenv** | 1.2.3 |
| **Ollama** | Local |
| **Model** | Qwen3 8B |

> As versões das dependências Python estão fixadas no arquivo `requirements.txt`.

---

## Requirements

Antes de executar o projeto, certifique-se de ter instalado:

- [asdf](https://asdf-vm.com/)
- Python 3.11.9
- `pip`
- [Ollama](https://ollama.com/)

---

## Installation

### 1. Clone o projeto
```bash
git clone <repository-url>
cd incident-agent
```

### 2. Configure o Python

O projeto utiliza **Python 3.11.9**.

```bash
asdf install python 3.11.9
asdf local python 3.11.9
```

Verifique se a versão está correta:
```bash
python --version
# Resultado esperado: Python 3.11.9
```

O comando `asdf local` criará o arquivo `.tool-versions`:
```text
python 3.11.9
```

### 3. Crie o ambiente virtual
```bash
python -m venv .venv
```

Ative o ambiente virtual:

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```cmd
  .venv\Scripts\activate
  ```

### 4. Instale as dependências
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Ollama

O projeto utiliza o **Ollama** para executar o modelo de linguagem localmente.

1. **Verifique se está instalado:**
   ```bash
   ollama --version
   ```

2. **Baixe o modelo:**
   ```bash
   ollama pull qwen3:1.7b
   ```

3. **Verifique os modelos disponíveis:**
   ```bash
   ollama list
   ```

4. **Teste o modelo:**
   ```bash
   ollama run qwen3:1.7b
   ```
   *(Para sair, digite `/bye`)*

---

## Configuration

Crie o arquivo `.env` na raiz do projeto:

```env
OLLAMA_MODEL=qwen3:1.7b
MAX_RETRIES=2
```

### Environment Variables

| Variável | Descrição | Default |
| :--- | :--- | :--- |
| `OLLAMA_MODEL` | Modelo utilizado pelo agente | `qwen3:1.7b` |
| `MAX_RETRIES` | Número máximo de tentativas | `2` |

---

## Usage

Com o ambiente virtual ativado, execute:

```bash
python app.py
```

A aplicação solicitará a descrição de um incidente:

```text
Descreva o incidente:
> 
```

**Exemplo:**
```text
O banco de produção está apresentando muitos deadlocks.
```

### Fluxo de Execução

```text
Incident
   │
   ▼
Classifier
   │
   ├── DB ──► DB Tool ──┐
   │                    │
   └── OPS ─► OPS Tool ─┤
                        │
                        ▼
                    Validator
                        │
                  ┌─────┴─────┐
                  │           │
               Success      Failure
                  │           │
                  ▼           ▼
                 END         Retry
                              │
                              ▼
                          Classifier
```

---

## Example

### Exemplo 1: DB

**Entrada:**
```text
O banco de produção está apresentando muitos deadlocks.
```

**Saída esperada:**
```text
[CLASSIFIER]
Area: db

[DB NODE]
[DB TOOL] Executando 'analyze_and_fix' em 'production-db'

[VALIDATOR]
Success: True
```

### Exemplo 2: OPS

**Entrada:**
```text
O serviço de pagamentos está retornando HTTP 503.
```

Nesse caso, o incidente deverá ser direcionado automaticamente para a área de **OPS**.

---

## Project Structure

```text
incident-agent/
│
├── .env
├── .gitignore
├── .tool-versions
├── README.md
├── requirements.txt
│
├── app.py
├── config.py
├── state.py
│
├── agents/
│   ├── __init__.py
│   ├── classifier.py
│   └── validator.py
│
├── graph/
│   ├── __init__.py
│   ├── builder.py
│   ├── edges.py
│   └── nodes.py
│
└── tools/
    ├── __init__.py
    ├── db.py
    └── ops.py
```

---

## Modules

- **`app.py`**: Entry point da aplicação. Responsável por receber o incidente, inicializar o estado e executar o grafo.
- **`agents/classifier.py`**: Responsável pela classificação do incidente (`DB` ou `OPS`).
- **`agents/validator.py`**: Analisa o resultado retornado pela tool e determina se a execução foi satisfatória.
- **`tools/db.py`**: Tools relacionadas a operações de banco de dados (atualmente com implementação simulada).
- **`tools/ops.py`**: Tools relacionadas a operações de infraestrutura (atualmente com implementação simulada).
- **`graph/nodes.py`**: Implementação dos nodes do LangGraph.
- **`graph/edges.py`**: Implementação das regras de roteamento e retry.
- **`graph/builder.py`**: Responsável por construir e compilar o `StateGraph`.
- **`state.py`**: Define o estado compartilhado entre os nodes.
- **`config.py`**: Centraliza as configurações da aplicação.

---

## Development

Para trabalhar no projeto, lembre-se de ativar o ambiente virtual:

```bash
source .venv/bin/activate
python --version
python app.py
```

---

## Current Limitations

Este projeto é um **Proof of Concept (PoC)**. Atualmente:

- As tools de `DB` e `OPS` são simuladas.
- As tools retornam apenas sucesso.
- Não existe integração real com infraestrutura.
- Não existe integração real com banco de dados.
- Não existe persistência do estado.
- Não existem testes automatizados.
- O retry está implementado na estrutura do grafo, mas ainda não é exercitado por falhas reais.

---

## Roadmap

Próximas evoluções planejadas:

- [ ] Simular falhas nas tools.
- [ ] Melhorar estratégia de retry.
- [ ] Permitir que o agente escolha dinamicamente a ação.
- [ ] Criar múltiplas tools para DB.
- [ ] Criar múltiplas tools para OPS.
- [ ] Adicionar tratamento de exceções.
- [ ] Adicionar persistência do estado.
- [ ] Adicionar *human-in-the-loop*.
- [ ] Adicionar observabilidade.
- [ ] Transformar DB e OPS em subgrafos.
- [ ] Integrar ferramentas reais de infraestrutura.
- [ ] Adicionar testes automatizados.

---

## License

Este projeto é experimental e destinado a estudos e prototipação.