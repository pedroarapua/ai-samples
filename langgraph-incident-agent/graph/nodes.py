from typing import Any

from agents.classifier import classify_incident
from agents.tool_selector import select_tool
from agents.validator import validate_execution

from state import IncidentState

from tools.registry import (
    DB_TOOLS,
    OPS_TOOLS,
)


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

    return execute_tool_node(
        state,
        DB_TOOLS,
    )


def execute_ops_node(
    state: IncidentState,
) -> IncidentState:

    return execute_tool_node(
        state,
        OPS_TOOLS,
    )


def execute_tool_node(
    state: IncidentState,
    tools: dict[str, Any],
) -> IncidentState:

    print("\n[TOOL SELECTOR]")

    available_tools = list(
        tools.keys()
    )

    previous_tool_output = state.get(
        "tool_output"
    )

    selection = select_tool(
        incident=state["incident"],
        area=state["area"],
        available_tools=available_tools,
        previous_tool_output=previous_tool_output,
    )

    print(
        f"Selected tool: "
        f"{selection.tool_name}"
    )

    print(
        f"Reason: "
        f"{selection.reason}"
    )

    tool = tools.get(
        selection.tool_name
    )

    if tool is None:
        raise ValueError(
            f"Tool inválida selecionada: "
            f"{selection.tool_name}"
        )

    tool_input = build_tool_input(
        state,
        selection.tool_name,
    )

    print("\n[TOOL]")
    print(
        f"Executing: "
        f"{selection.tool_name}"
    )

    result = tool.invoke(
        tool_input
    )

    print(f"Result: {result}")

    return {
        "selected_tool": selection.tool_name,
        "tool_selection_reason": selection.reason,
        "tool_input": tool_input,
        "tool_output": result,
    }


def build_tool_input(
    state: IncidentState,
    tool_name: str,
) -> dict[str, Any]:

    if state["area"] == "db":
        return {
            "target": "production-db",
        }

    return {
        "service": "api",
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