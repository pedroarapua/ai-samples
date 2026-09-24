from typing import Any, Literal

from typing_extensions import TypedDict


Area = Literal["db", "ops"]


class IncidentState(TypedDict, total=False):
    # -----------------------------------------
    # Incidente original
    # -----------------------------------------

    incident: str

    # -----------------------------------------
    # Resultado da classificação
    # -----------------------------------------

    area: Area
    classification_reason: str

    # -----------------------------------------
    # Tool selecionada
    # -----------------------------------------

    selected_tool: str
    tool_selection_reason: str

    # -----------------------------------------
    # Dados da execução da tool
    # -----------------------------------------

    tool_input: dict[str, Any]
    tool_output: dict[str, Any]

    # -----------------------------------------
    # Resultado da validação
    # -----------------------------------------

    execution_success: bool
    validation_reason: str

    # -----------------------------------------
    # Controle de tentativas
    # -----------------------------------------

    retry_count: int