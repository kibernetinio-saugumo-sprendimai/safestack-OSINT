from core_control.module_contract import ModuleContract
from core_control.context import Context
from core_control.result import Result
from core_control.exceptions import ModuleExecutionError


class WhoisRDAPAdapter(ModuleContract):
    """
    Adapter for WHOIS/RDAP OSINT module.
    """

    name = "whois.rdap"

    def run(self, context: Context) -> Result:
        try:
            try:
                from modules.whois_rdap.module import WhoisRDAPModule
            except ModuleNotFoundError as exc:
                raise ModuleExecutionError(
                    "Whois/RDAP module requires the 'requests' package. Install it with: pip install requests"
                ) from exc

            module = WhoisRDAPModule()

            raw_data = module.run(context.target)

            # Dynamic confidence scoring
            confidence = 0.8  # Default
            source = raw_data.get("source", "unknown")

            if raw_data.get("error"):
                confidence = 0.0
            elif source == "rdap.org":
                confidence = 0.95
            elif source == "bootstrap":
                confidence = 0.85

            return Result(
                module=self.name,
                target=context.target,
                data=raw_data,
                confidence=confidence,
                sources=[source] if source != "unknown" else ["rdap"],
            )

        except Exception as exc:
            raise ModuleExecutionError(
                f"WhoisRDAP adapter failed: {exc}"
            ) from exc
