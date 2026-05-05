import json
from core_control.result import Result


def format_result(result: Result, fmt: str = "pretty") -> str:
    if fmt == "json":
        return json.dumps(
            {
                "module": result.module,
                "target": result.target,
                "data": result.data,
                "confidence": result.confidence,
                "sources": result.sources,
                "timestamp": result.timestamp.isoformat(),
            },
            indent=2,
            sort_keys=True,
        )

    # default: pretty
    lines = [
        f"Module     : {result.module}",
        f"Target     : {result.target}",
        f"Confidence : {result.confidence}",
        f"Sources    : {', '.join(result.sources)}",
        f"Timestamp  : {result.timestamp.isoformat()}",
        "",
        "Data:",
        json.dumps(result.data, indent=2),
    ]
    return "\n".join(lines)
