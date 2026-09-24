from langgraph.graph import END, START, StateGraph

from graph.edges import (
    increment_retry,
    route_after_retry,
    route_after_validation,
    route_by_area,
)

from graph.nodes import (
    classify_node,
    execute_db_node,
    execute_ops_node,
    validate_node,
)

from state import IncidentState


def build_graph():

    builder = StateGraph(
        IncidentState
    )

    # -----------------------------------------
    # Nodes
    # -----------------------------------------

    builder.add_node(
        "classify",
        classify_node,
    )

    builder.add_node(
        "execute_db",
        execute_db_node,
    )

    builder.add_node(
        "execute_ops",
        execute_ops_node,
    )

    builder.add_node(
        "validate",
        validate_node,
    )

    builder.add_node(
        "increment_retry",
        increment_retry,
    )

    # -----------------------------------------
    # Entrada
    # -----------------------------------------

    builder.add_edge(
        START,
        "classify",
    )

    # -----------------------------------------
    # Classificação
    # -----------------------------------------

    builder.add_conditional_edges(
        "classify",
        route_by_area,
        {
            "db": "execute_db",
            "ops": "execute_ops",
        },
    )

    # -----------------------------------------
    # Execução
    # -----------------------------------------

    builder.add_edge(
        "execute_db",
        "validate",
    )

    builder.add_edge(
        "execute_ops",
        "validate",
    )

    # -----------------------------------------
    # Validação
    # -----------------------------------------

    builder.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "success": END,
            "retry": "increment_retry",
            "failure": END,
        },
    )

    # -----------------------------------------
    # Retry
    # -----------------------------------------

    builder.add_conditional_edges(
        "increment_retry",
        route_after_retry,
        {
            "db": "execute_db",
            "ops": "execute_ops",
        },
    )

    return builder.compile()