from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from config import OLLAMA_MODEL


class ToolSelection(BaseModel):
    tool_name: str = Field(
        description=(
            "Nome exato da ferramenta que deve "
            "ser executada."
        )
    )

    reason: str = Field(
        description=(
            "Motivo da escolha da ferramenta."
        )
    )


llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0,
)


tool_selector = llm.with_structured_output(
    ToolSelection
)


def select_tool(
    incident: str,
    area: str,
    available_tools: list[str],
    previous_tool_output: dict | None = None,
) -> ToolSelection:

    prompt = f"""
Você é um agente responsável por escolher
a próxima ferramenta para tratar um incidente
de TI.

Incidente:

{incident}

Área responsável:

{area}

Ferramentas disponíveis:

{available_tools}

Resultado da execução anterior:

{previous_tool_output}

Escolha SOMENTE uma das ferramentas
disponíveis.

Regras:

1. Não invente o nome de uma ferramenta.
2. Escolha a ferramenta mais adequada para
   investigar ou resolver o incidente.
3. Se houver um resultado de execução anterior,
   considere esse resultado para escolher
   a próxima ação.
4. Explique brevemente o motivo da escolha.

Retorne o nome exato da ferramenta escolhida.
"""

    return tool_selector.invoke(
        prompt
    )