import time
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

class SemanticCache:
    def __init__(self):
        print("Carregando modelo de embeddings moderno local...")
        # Modelo leve de 384 dimensões, ideal para rodar rápido na CPU do Kubuntu
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Conexão apontando para o localhost (Docker exposto na porta 5432)
        self.conn = psycopg2.connect(
            host="localhost",
            dbname="semantic_cache_db",
            user="postgres",
            password="postgres"
        )
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        """Inicializa as extensões e tabelas necessárias no Postgres"""
        self.cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        register_vector(self.conn)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache_store (
                id SERIAL PRIMARY KEY,
                pergunta TEXT UNIQUE,
                resposta TEXT,
                embedding vector(384)
            );
        """)

        self.cursor.execute("""
            DELETE FROM cache_store;
        """)
        self.conn.commit()

    def buscar(self, nova_pergunta, threshold=0.50):
        """
        Busca por similaridade usando o operador de distância de cosseno (<=>).
        Menor distância = maior similaridade semântica.
        """
        vetor = self.model.encode(nova_pergunta)
        
        self.cursor.execute("""
            SELECT pergunta, resposta, embedding <=> %s AS distancia 
            FROM cache_store 
            ORDER BY distancia ASC LIMIT 1;
        """, (vetor,))
        
        resultado = self.cursor.fetchone()
        
        if resultado:
            distancia_real = resultado[2]
            print(f"   [Debug Cache]: Menor distância matemática no banco: {distancia_real:.4f}")
            
            # Se a distância for menor que o limite tolerado, é um HIT
            if distancia_real < threshold:
                return {
                    "pergunta_original": resultado[0],
                    "resposta": resultado[1],
                    "distancia": distancia_real,
                    "hit": True
                }
        return {"hit": False}

    def salvar(self, pergunta, resposta):
        """Salva a pergunta e seu vetor correspondente no banco"""
        vetor = self.model.encode(pergunta)
        try:
            self.cursor.execute("""
                INSERT INTO cache_store (pergunta, resposta, embedding) 
                VALUES (%s, %s, %s)
                ON CONFLICT (pergunta) DO NOTHING;
            """, (pergunta, resposta, vetor))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao salvar no cache: {e}")

    def fechar(self):
        self.cursor.close()
        self.conn.close()

# --- Fluxo de Teste Exemplo ---
if __name__ == "__main__":
    cache = SemanticCache()

    # Pergunta 1: Cenário de Inclusão no Cache (CACHE MISS)
    p1 = "Como eu faço para trocar a minha senha?"
    print(f"\n[Usuário 1]: '{p1}'")
    
    busca1 = cache.buscar(p1, threshold=0.50)
    if not busca1["hit"]:
        print("-> Cache Miss! Simulando processamento pesado da IA...")
        time.sleep(2.5)  # Simula delay da rede/API real
        resposta_ia = "Vá em Perfil > Segurança > Alterar Senha."
        cache.salvar(p1, resposta_ia)
        print(f"-> Resposta da IA: {resposta_ia}")

    # Pergunta 2: Variante Semântica (Agora calibrada para dar CACHE HIT)
    p2 = "esqueci minha senha, onde troco?"
    print(f"\n[Usuário 2]: '{p2}'")
    
    start_time = time.time()
    busca2 = cache.buscar(p2, threshold=0.50)
    end_time = time.time()

    if busca2["hit"]:
        print(f"-> Cache HIT Semântico! (Distância: {busca2['distancia']:.4f})")
        print(f"-> Pergunta que ativou o cache: '{busca2['pergunta_original']}'")
        print(f"-> Resposta recuperada: {busca2['resposta']}")
        print(f"-> Tempo de resposta do cache: {(end_time - start_time) * 1000:.2f}ms")
    else:
        print("-> Cache Miss!")

    cache.fechar()
