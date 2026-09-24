from config import MAX_RETRIES

from state import IncidentState


def route_by_area(
    state: IncidentState,
) -> str:

    return state["area"]


def route_after_validation(
    state: IncidentState,
) -> str:

    if state["execution_success"]:
        return "success"

    retry_count = state.get(
        "retry_count",
        0,
    )

    if retry_count >= MAX_RETRIES:
        return "failure"

    return "retry"


def route_after_retry(
    state: IncidentState,
) -> str:

    return state["area"]


def increment_retry(
    state: IncidentState,
) -> IncidentState:

    retry_count = state.get(
        "retry_count",
        0,
    )

    return {
        "retry_count": retry_count + 1,
    }