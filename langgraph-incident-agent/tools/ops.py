from typing import Any

from langchain_core.tools import tool


@tool
def check_service_health(
    service: str,
) -> dict[str, Any]:
    """
    Verifica a saúde de um serviço.
    """

    print(
        f"[OPS TOOL] Verificando saúde "
        f"do serviço '{service}'"
    )

    return {
        "status": "success",
        "area": "ops",
        "action": "check_service_health",
        "service": service,
        "message": (
            f"Saúde do serviço '{service}' "
            "verificada com sucesso."
        ),
    }


@tool
def check_pods(
    service: str,
) -> dict[str, Any]:
    """
    Verifica os pods relacionados a um serviço.
    """

    print(
        f"[OPS TOOL] Verificando pods "
        f"do serviço '{service}'"
    )

    return {
        "status": "success",
        "area": "ops",
        "action": "check_pods",
        "service": service,
        "message": (
            f"Pods do serviço '{service}' "
            "verificados com sucesso."
        ),
    }


@tool
def restart_service(
    service: str,
) -> dict[str, Any]:
    """
    Reinicia um serviço.
    """

    print(
        f"[OPS TOOL] Reiniciando "
        f"o serviço '{service}'"
    )

    return {
        "status": "success",
        "area": "ops",
        "action": "restart_service",
        "service": service,
        "message": (
            f"Serviço '{service}' "
            "reiniciado com sucesso."
        ),
    }