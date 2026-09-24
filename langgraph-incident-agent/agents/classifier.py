from typing import Literal

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from config import OLLAMA_MODEL


class IncidentClassification(BaseModel):
    area: Literal["db", "ops"] = Field(
        description="Área responsável pelo incidente."
    )

    reason: str = Field(
        description="Motivo da classificação."
    )


llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0,
)


classifier = llm.with_structured_output(
    IncidentClassification
)


def classify_incident(
    incident: str,
) -> IncidentClassification:

    prompt = f"""
Você é um especialista em classificação
de incidentes de TI.

Sua tarefa é determinar qual área deve
receber o incidente.

As áreas disponíveis são:

DB
- Banco de dados
- SQL
- Queries
- Deadlocks
- Locks
- Conexões de banco
- Replicação
- Performance de banco

OPS
- Kubernetes
- Containers
- Deploy
- CPU
- Memória
- Disco
- Rede
- Serviços
- Infraestrutura

Incidente recebido:

{incident}

Classifique o incidente em somente uma
das seguintes áreas:

db
ops

Também explique brevemente o motivo
da classificação.
"""

    return classifier.invoke(prompt)
