from typing import Any

from langchain_core.tools import tool


@tool
def execute_db_action(
    action: str,
    target: str,
) -> dict[str, Any]:
    """
    Executa uma ação relacionada a banco de dados.
    """

    print(
        f"[DB TOOL] Executando '{action}' "
        f"em '{target}'"
    )

    # Simulação.
    #
    # Futuramente podemos substituir isso
    # por uma chamada real ao banco de dados.

    return {
        "status": "success",
        "area": "db",
        "action": action,
        "target": target,
        "message": (
            f"Ação '{action}' executada "
            f"com sucesso em '{target}'."
        ),
    }
