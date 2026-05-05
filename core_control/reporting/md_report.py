from core_control.result import Result


def generate_md_report(target: str, results: dict) -> str:
    lines = []

    lines.append("# SafeStack OSINT Report")
    lines.append("")
    lines.append(f"**Target:** `{target}`")
    lines.append("")

    meta = results.get("_meta", {})
    if meta:
        lines.append("## Overall Confidence")
        lines.append(
            f"- **Target confidence:** `{meta.get('target_confidence')}`")
        lines.append("")

    lines.append("## Module Results")

    for name, res in results.items():
        if name == "_meta":
            continue

        lines.append(f"### {name}")

        if isinstance(res, Result):
            lines.append(f"- Confidence: `{res.confidence}`")
            lines.append(f"- Sources: `{', '.join(res.sources)}`")
            lines.append("")
            lines.append("```json")
            lines.append(str(res.data))
            lines.append("```")
        else:
            lines.append(f"- ❌ Error: `{res.get('error')}`")
            if "reason" in res:
                lines.append(f"  - {res['reason']}")

        lines.append("")

    return "\n".join(lines)
