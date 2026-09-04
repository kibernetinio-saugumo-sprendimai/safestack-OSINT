from core_control.module_contract import ModuleContract
from core_control.context import Context
from core_control.result import Result
from core_control.exceptions import ModuleExecutionError


class PassiveDNSAdapter(ModuleContract):
    """
    Adapter that wraps the existing passive_dns module
    and exposes it via the core_control contract.
    """

    name = "dns.live"

    def validate(self, context: Context) -> None:
        if context.mode not in context.policy.allowed_modes:
            raise ValueError(f"Mode '{context.mode}' not allowed for module '{self.name}'")

    def run(self, context: Context) -> Result:
        try:
            try:
                from modules.passive_dns.module import PassiveDNSModule
            except ModuleNotFoundError as exc:
                raise ModuleExecutionError(
                    "PassiveDNS module requires the 'dnspython' package. Install it with: pip install dnspython"
                ) from exc

            module = PassiveDNSModule()

            # Call existing module logic
            raw_data = module.run(context.target)

            # Dynamic confidence scoring
            confidence = 0.7  # Default
            source = raw_data.get("source", "unknown")

            if source == "local_dns":
                if raw_data.get("error") == "NXDOMAIN":
                    confidence = 1.0  # High certainty for NXDOMAIN
                else:
                    confidence = 0.9  # Real DNS data
            if raw_data.get("error"):
                confidence = 0.0

            return Result(
                module=self.name,
                target=context.target,
                data=raw_data,
                confidence=confidence,
                sources=[source],
            )

        except Exception as exc:
            raise ModuleExecutionError(
                f"PassiveDNS adapter failed: {exc}"
            ) from exc
