from typing import Dict, List
from core_control.context import Context
from core_control.registry import ModuleRegistry
from core_control.result import Result
from core_control.exceptions import ModuleExecutionError
from core_control.risk import RiskEngine
from core_control.audit_log import AuditLogger


class Runner:
    """
    Execution runner responsible for controlled module invocation.
    """

    def __init__(self, registry: ModuleRegistry) -> None:
        self.registry = registry
        self.audit_logger = AuditLogger()

    def run(self, module_name: str, context: Context) -> Result:
        try:
            module_cls = self.registry.get(module_name, context)
            module = module_cls()
            module.validate(context)

            result = module.run(context)
            if not isinstance(result, Result):
                raise TypeError("Module did not return a Result object")

            self.audit_logger.log_execution(
                target=context.target,
                module_name=module_name,
                status="SUCCESS" if "error" not in result.data else "WARNING",
                result_summary={
                    "confidence": result.confidence,
                    "sources": result.sources,
                    "has_error": "error" in result.data
                }
            )

            return result

        except Exception as exc:
            self.audit_logger.log_execution(
                target=context.target,
                module_name=module_name,
                status="FAILED",
                result_summary={"error": str(exc)}
            )
            raise ModuleExecutionError(
                f"Execution failed for module '{module_name}': {exc}"
            ) from exc

    def run_all(self, context: Context) -> Dict:
        results: List[Result] = []
        errors: Dict[str, str] = {}

        for module_name in self.registry.list_modules():
            try:
                result = self.run(module_name, context)
                results.append(result)
            except ModuleExecutionError as exc:
                errors[module_name] = str(exc)

        meta = {
            "target_confidence": RiskEngine.compute_target_confidence(results),
            "flags": RiskEngine.extract_flags(results),
        }

        meta["hints"] = RiskEngine.generate_hints(meta["flags"])

        return {
            "results": results,
            "errors": errors,
            "meta": meta,
        }
