# Semantic Cache com PostgreSQL (pgvector) e Python

Este subprojeto faz parte do monorepo **[ai-samples](https://github.com)** e demonstra a implementação prática de um **Cache Semântico (Semantic Caching)** voltado para Engenharia de IA. O objetivo é interceptar perguntas de usuários e, por meio de busca vetorial por proximidade, responder requisições similares instantaneamente, economizando custos de tokens de APIs de LLMs e reduzindo a latência para menos de 5ms.

## 🚀 Como Funciona o Cache Semântico?

Diferente do cache tradicional baseado em strings exatas (chave-valor), o cache semântico utiliza **Embeddings** para entender o *significado* da pergunta:
1. O usuário faz uma pergunta variante (ex: `"esqueci meu password, onde altero?"`).
2. A aplicação gera um vetor matemático dessa frase usando um modelo local de NLP (`all-MiniLM-L6-v2`).
3. O banco de dados PostgreSQL, através da extensão `pgvector`, calcula a **distância de cosseno (`<=>`)** contra as perguntas já respondidas no banco.
4. Se o significado for estatisticamente próximo (abaixo do limiar/threshold definido), o sistema retorna a resposta gravada no banco imediatamente, sem acionar o modelo de IA pesado.

---

## 🛠️ Tecnologias e Ambiente

O ambiente é gerenciado de forma declarativa e automatizada para garantir reprodutibilidade:
* **Gerenciador de Versão:** `asdf` (através do arquivo `.tool-versions` incluso no repositório)
* **Banco de Dados:** PostgreSQL 17 com extensão `pgvector` via Docker Compose (v1)
* **Modelo de Embeddings:** `sentence-transformers` (Local e gratuito, rodando em CPU)
* **Driver de Banco:** `psycopg2-binary`

---

## 💻 Configuração do Ambiente Local

### 1. Pré-requisitos
Certifique-se de ter o `asdf` instalado no terminal e o serviço do Docker ativo.

### 2. Clonar o Repositório e Acessar o Projeto
```bash
git clone https://github.com/pedroarapua/ai-samples.git
cd ai-samples/sematic-cache

# Instala as ferramentas declaradas no arquivo .tool-versions
asdf install
```

### 3. Configurar e Instalar Dependências do Python
```bash
# Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate

# Atualizar o pip e instalar os pacotes modernos
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Subir o Banco de Dados (Docker Compose)
Inicialize o container do PostgreSQL já configurado com a extensão vetorial:
```bash
docker-compose up -d
```

---

## 🏃‍♂️ Executando o Teste de Validação

Para rodar a simulação e comprovar a diferença de performance física entre um **Cache Miss** (chamada à IA) e um **Cache Hit** (recuperação semântica):

```bash
python app.py
```

### O que você verá no output:
* **Usuário 1:** Faz a pergunta `"Como eu faço para trocar a minha senha?"` → O sistema detecta um **Cache Miss**, simula o delay da API de IA (2.5 segundos) e salva o resultado no banco.
* **Usuário 2:** Pergunta `"esqueci meu password, onde altero?"` → Mesmo usando termos diferentes (como a palavra em inglês *password*), o `pgvector` detecta um **Cache HIT Semântico** e entrega a resposta em **poucos milissegundos**.

---

## 📂 Estrutura do Subprojeto

```text
ai-samples/
└── sematic-cache/
    ├── .tool-versions     # Versão declarativa do Python (3.11.9) para asdf
    ├── docker-compose.yml # Container estável do PostgreSQL + pgvector
    ├── requirements.txt   # Dependências modernas e estáveis
    ├── app.py             # Classe SemanticCache e fluxo de execução
    └── README.md          # Documentação do projeto
```
