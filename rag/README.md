# Retrieval-Augmented Generation (RAG) Híbrido com pgvector e Gemini

Este subprojeto faz parte do monorepo **[ai-samples](https://github.com)** e demonstra a implementação prática de uma arquitetura **RAG (Retrieval-Augmented Generation)** altamente eficiente e otimizada para custo. 

A arquitetura foi desenhada de forma híbrida: a busca semântica é feita localmente na máquina (sem custos de API) e apenas a síntese final é enviada para a camada gratuita do Google Gemini, eliminando problemas de limite de créditos de provedores pagos.

## 🚀 Como Funciona a Arquitetura?

1. **Ingestão e Limpeza:** O script limpa automaticamente tabelas com dimensões conflitantes antigas e fatia o arquivo `conhecimento.txt` em pequenos blocos (*chunks*).
2. **Embeddings Locais (Grátis):** Cada bloco de texto é transformado em um vetor de 384 dimensões usando o modelo `sentence-transformers/all-MiniLM-L6-v2` rodando localmente na CPU via Hugging Face.
3. **Persistência no pgvector:** Os vetores são armazenados no PostgreSQL 17 através da extensão `pgvector`.
4. **Geração Híbrida:** A pergunta do usuário gera um embedding local, o `pgvector` busca as duas maiores similaridades e envia apenas esse contexto enxuto para o modelo `gemini-3.5-flash-lite` gerar a resposta final estruturada.

---

## 🛠️ Tecnologias e Ambiente

* **Gerenciador de Versão:** `asdf` (Python 3.11.9 declarado no `.tool-versions`).
* **Banco de Dados:** PostgreSQL 17 com extensão `pgvector` via Docker Compose.
* **Embeddings:** `langchain-huggingface` (Processamento local na CPU).
* **LLM de Síntese:** `langchain-google-genai` (Modelo Gemini 3.5 Flash-Lite).

---

## 💻 Configuração do Ambiente Local

### 1. Preparar o Subprojeto
```bash
cd ai-samples/rag
asdf install
```

### 2. Configurar o Ambiente Virtual e Dependências
```bash
python -m venv venv
source venv/bin/activate

# Atualiza as ferramentas essenciais e instala os pacotes forçando binários
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --only-binary :all:
```

### 3. Subir o Banco Vetorial
```bash
docker compose up -d
```

### 4. Executar a Aplicação
Obtenha uma chave gratuita no Google AI Studio, exporte no terminal e execute:
```bash
export GEMINI_API_KEY="sua_chave_gemini_aqui"
python app.py
```

---

## 📂 Estrutura Atualizada do Diretório

```text
ai-samples/
└── rag/
    ├── .tool-versions     # Configuração declarativa do Python para asdf
    ├── docker-compose.yml # Container estável do PostgreSQL 17 + pgvector
    ├── requirements.txt   # Dependências modernas, incluindo splitters e classic
    ├── conhecimento.txt   # Base de dados local (Fonte da verdade)
    ├── app.py             # Pipeline RAG completo com correção de AFC do Google
    └── README.md          # Esta documentação atualizada
```
