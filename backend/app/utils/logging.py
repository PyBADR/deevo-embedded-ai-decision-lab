import logging
import json
import uuid
from contextvars import ContextVar
from datetime import datetime

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger

def get_trace_id() -> str:
    tid = trace_id_var.get()
    if not tid:
        tid = str(uuid.uuid4())
        trace_id_var.set(tid)
    return tid

def set_trace_id(tid: str):
    trace_id_var.set(tid)

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": get_trace_id()
        }
        return json.dumps(log_data)
