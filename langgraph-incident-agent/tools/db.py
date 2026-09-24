from typing import Any

from langchain_core.tools import tool


@tool
def check_db_connections(
    target: str,
) -> dict[str, Any]:
    """
    Verifica as conexões ativas do banco de dados.
    """

    print(
        f"[DB TOOL] Verificando conexões "
        f"em '{target}'"
    )

    return {
        "status": "success",
        "area": "db",
        "action": "check_db_connections",
        "target": target,
        "message": (
            f"Conexões do banco '{target}' "
            "verificadas com sucesso."
        ),
    }


@tool
def check_db_locks(
    target: str,
) -> dict[str, Any]:
    """
    Verifica locks ativos no banco de dados.
    """

    print(
        f"[DB TOOL] Verificando locks "
        f"em '{target}'"
    )

    return {
        "status": "success",
        "area": "db",
        "action": "check_db_locks",
        "target": target,
        "message": (
            f"Locks do banco '{target}' "
            "verificados com sucesso."
        ),
    }


@tool
def check_slow_queries(
    target: str,
) -> dict[str, Any]:
    """
    Verifica queries lentas no banco de dados.
    """

    print(
        f"[DB TOOL] Verificando queries lentas "
        f"em '{target}'"
    )

    return {
        "status": "success",
        "area": "db",
        "action": "check_slow_queries",
        "target": target,
        "message": (
            f"Queries lentas do banco '{target}' "
            "verificadas com sucesso."
        ),
    }