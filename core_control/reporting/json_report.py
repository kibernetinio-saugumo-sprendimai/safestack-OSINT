from core_control.result import Result
from datetime import datetime


def generate_json_report(target: str, results: list, errors: dict = None, meta: dict = None) -> dict:
    """
    Generate a JSON-serializable report structure.
    """
    modules_data = {}

    for res in results:
        if isinstance(res, Result):
            modules_data[res.module] = {
                "confidence": res.confidence,
                "sources": res.sources,
                "data": res.data,
                "timestamp": res.timestamp.isoformat()
            }

    if errors:
        for name, err in errors.items():
            modules_data[name] = {
                "error": err
            }

    report = {
        "target": target,
        "generated_at": datetime.utcnow().isoformat(),
        "modules": modules_data,
        "meta": meta or {}
    }

    return report
