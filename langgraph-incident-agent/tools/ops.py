from typing import Any

from langchain_core.tools import tool


@tool
def execute_ops_action(
    action: str,
    service: str,
) -> dict[str, Any]:
    """
    Executa uma ação relacionada à infraestrutura.
    """

    print(
        f"[OPS TOOL] Executando '{action}' "
        f"no serviço '{service}'"
    )

    # Simulação.
    #
    # Futuramente podemos substituir isso
    # por chamadas reais de infraestrutura.

    return {
        "status": "success",
        "area": "ops",
        "action": action,
        "service": service,
        "message": (
            f"Ação '{action}' executada "
            f"com sucesso no serviço '{service}'."
        ),
    }
