from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from config import OLLAMA_MODEL


class ValidationResult(BaseModel):
    success: bool = Field(
        description=(
            "Indica se a execução foi satisfatória "
            "e resolveu o incidente."
        )
    )

    reason: str = Field(
        description="Explicação da decisão."
    )


llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0,
)


validator = llm.with_structured_output(
    ValidationResult
)


def validate_execution(
    incident: str,
    tool_output: dict,
) -> ValidationResult:

    prompt = f"""
Você é responsável por validar a execução
de uma ação de resolução de incidente.

Incidente original:

{incident}

Resultado retornado pela ferramenta:

{tool_output}

Determine se a execução foi satisfatória.

Analise:

1. A ferramenta executou corretamente?
2. O resultado indica sucesso?
3. Existe alguma evidência de erro?
4. Existe evidência suficiente para considerar
   o incidente resolvido?

Retorne:

success=true

somente quando houver evidência suficiente
de sucesso.

Caso contrário:

success=false

Explique brevemente sua decisão.
"""

    return validator.invoke(prompt)
