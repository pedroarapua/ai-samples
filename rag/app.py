import os
import psycopg
import warnings
# Silencia os avisos informativos da Hugging Face
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")

from langchain_huggingface import HuggingFaceEmbeddings
# SUBSTITUÍDO: OpenAI por Google GenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_postgres import PGVector
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# 1. Validação da Chave de API do Gemini
if "GEMINI_API_KEY" not in os.environ:
    raise ValueError("Por favor, defina a variável de ambiente 'GEMINI_API_KEY'.")

# 2. Configurações de Conexão (Postgres 17 + pgvector)
CONNECTION_STRING = "postgresql+psycopg://postgres:postgres@localhost:5432/rag_db"
COLLECTION_NAME = "politicas_locais_empresa"

# Funções de limpeza permanecem aqui...
def limpar_colecoes_antigas(connection_uri):
    print("🧹 Limpando o banco de dados para evitar conflitos de dimensões...")
    try:
        # O psycopg puro exige remover o '+psycopg' da string que o LangChain usa
        uri_psycopg_puro = connection_uri.replace("postgresql+psycopg://", "postgresql://")
        
        with psycopg.connect(uri_psycopg_puro) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS langchain_pg_embedding CASCADE;")
                cur.execute("DROP TABLE IF EXISTS langchain_pg_collection CASCADE;")
                print("✨ Tabelas antigas e coleções incompatíveis limpas com sucesso!")
    except Exception as e:
        print(f"⚠️ Aviso ao limpar tabelas: {e}")
        pass

limpar_colecoes_antigas(CONNECTION_STRING)

# 3. Inicializar Embeddings Locais (Grátis)
print("\n🔄 Carregando modelo de embedding local...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Conectar ao pgvector
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    use_jsonb=True
)

# 5. Ingestão de Dados
with open("conhecimento.txt", "r", encoding="utf-8") as f:
    texto_puro = f.read()

documento_base = [Document(page_content=texto_puro)]
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
texts = text_splitter.split_documents(documento_base)
vector_store.add_documents(texts)
print(f"✅ Documentos salvos no pgvector!")

# =====================================================================
# 6. CONFIGURAR A LLM GRATUITA (Google Gemini 3.5 Flash)
# =====================================================================
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
# =====================================================================


# 7. Fluxo RAG
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

system_prompt = (
    "Você é um assistente de atendimento interno. Use os seguintes trechos de contexto "
    "recuperados para responder à pergunta de forma direta. Se não souber a resposta baseada "
    "no contexto, diga 'Não encontrei essa informação no manual'.\n\n"
    "Contexto:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 8. Execução do Teste
pergunta = "Qual é a regra de reembolso para quem mora em São Paulo?"
print(f"\n🙋 Pergunta do usuário: '{pergunta}'")

resposta = rag_chain.invoke({"input": pergunta})
print(f"🤖 Resposta da IA: {resposta['answer']}\n")
