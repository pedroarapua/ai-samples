from tools.db import (
    check_db_connections,
    check_db_locks,
    check_slow_queries,
)

from tools.ops import (
    check_service_health,
    check_pods,
    restart_service,
)


DB_TOOLS = {
    "check_db_connections": check_db_connections,
    "check_db_locks": check_db_locks,
    "check_slow_queries": check_slow_queries,
}


OPS_TOOLS = {
    "check_service_health": check_service_health,
    "check_pods": check_pods,
    "restart_service": restart_service,
}