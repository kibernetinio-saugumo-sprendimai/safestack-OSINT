from core_control.module_contract import ModuleContract
from core_control.context import Context
from core_control.result import Result
from core_control.exceptions import ModuleExecutionError

from modules.tls_info.module import TLSInfoModule


class TLSInfoAdapter(ModuleContract):
    """
    Adapter for TLS information OSINT module.
    """

    name = "tls.info"

    def run(self, context: Context) -> Result:
        try:
            module = TLSInfoModule()

            raw_data = module.run(context.target)

            # Dynamic confidence scoring
            confidence = 0.9  # Default
            source = raw_data.get("source", "unknown")

            if raw_data.get("error"):
                confidence = 0.0
            elif source == "local_tls":
                confidence = 1.0

            return Result(
                module=self.name,
                target=context.target,
                data=raw_data,
                confidence=confidence,
                sources=[source] if source != "unknown" else ["tls"],
            )

        except Exception as exc:
            raise ModuleExecutionError(
                f"TLSInfo adapter failed: {exc}"
            ) from exc
