import json
import logging
import sys

class JSONFormatter(logging.Formatter):
    """Formats logs into clean structured JSON objects instead of long text sentences."""
    def format(self, record):
        log_data = {
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        if hasattr(record, "extra_metric"):
            log_data.update(record.extra_metric)
        return json.dumps(log_data)

logger = logging.getLogger("rag-app")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)