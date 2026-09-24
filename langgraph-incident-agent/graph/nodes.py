from agents.classifier import classify_incident
from agents.validator import validate_execution

from state import IncidentState

from tools.db import execute_db_action
from tools.ops import execute_ops_action


def classify_node(
    state: IncidentState,
) -> IncidentState:

    incident = state["incident"]

    print("\n[CLASSIFIER]")
    print(f"Incident: {incident}")

    result = classify_incident(
        incident
    )

    print(f"Area: {result.area}")
    print(f"Reason: {result.reason}")

    return {
        "area": result.area,
        "classification_reason": result.reason,
    }


def execute_db_node(
    state: IncidentState,
) -> IncidentState:

    print("\n[DB NODE]")

    result = execute_db_action.invoke(
        {
            "action": "analyze_and_fix",
            "target": "production-db",
        }
    )

    return {
        "tool_input": {
            "action": "analyze_and_fix",
            "target": "production-db",
        },
        "tool_output": result,
    }


def execute_ops_node(
    state: IncidentState,
) -> IncidentState:

    print("\n[OPS NODE]")

    result = execute_ops_action.invoke(
        {
            "action": "restart_service",
            "service": "api",
        }
    )

    return {
        "tool_input": {
            "action": "restart_service",
            "service": "api",
        },
        "tool_output": result,
    }


def validate_node(
    state: IncidentState,
) -> IncidentState:

    print("\n[VALIDATOR]")

    result = validate_execution(
        incident=state["incident"],
        tool_output=state["tool_output"],
    )

    print(f"Success: {result.success}")
    print(f"Reason: {result.reason}")

    return {
        "execution_success": result.success,
        "validation_reason": result.reason,
    }
