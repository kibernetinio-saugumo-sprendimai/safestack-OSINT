from adapters.tls_info.adapter import TLSInfoAdapter
from adapters.whois_rdap.adapter import WhoisRDAPAdapter
from adapters.passive_dns.adapter import PassiveDNSAdapter
from typing import Dict, Type

from core_control.context import Context
from core_control.module_contract import ModuleContract
from core_control.exceptions import PolicyViolationError


class ModuleRegistry:
    """
    Registry of all available OSINT modules.

    This class:
    - keeps track of registered modules
    - validates access based on execution policy
    - does NOT execute modules
    """

    def __init__(self) -> None:
        self._modules: Dict[str, Type[ModuleContract]] = {}

    def register(self, module_cls: Type[ModuleContract]) -> None:
        """
        Register a module class in the registry.

        The module MUST define a unique 'name' attribute.
        """
        name = getattr(module_cls, "name", None)
        if not name:
            raise ValueError("Module must define a non-empty 'name' attribute")

        if name in self._modules:
            raise ValueError(f"Module '{name}' is already registered")

        self._modules[name] = module_cls

    def is_allowed(self, module_name: str, context: Context) -> bool:
        """
        Check whether a module is allowed to run under current policy.
        """
        policy = context.policy

        # 1. Explicit deny-list has highest priority
        if policy.denied_modules is not None:
            if module_name in policy.denied_modules:
                return False

        # 2. Per-module mode restrictions (e.g. tls.info -> deep only)
        if policy.module_modes is not None:
            allowed_modes = policy.module_modes.get(module_name)
            if allowed_modes is not None:
                return context.mode in allowed_modes

        # 3. Global allow-list enforcement
        if policy.allowed_modules is not None:
            return module_name in policy.allowed_modules

        # 4.  Default: allowed
        return True

    def get(self, module_name: str, context: Context) -> Type[ModuleContract]:
        """
        Retrieve a module class if it is registered and allowed.
        """
        if module_name not in self._modules:
            raise KeyError(f"Module '{module_name}' is not registered")

        if not self.is_allowed(module_name, context):
            raise PolicyViolationError(
                f"Module '{module_name}' is not allowed by current policy"
            )

        return self._modules[module_name]

    def list_modules(self) -> Dict[str, Type[ModuleContract]]:
        """
        Return all registered modules.
        """
        return dict(self._modules)


# --- Adapter registrations (wiring layer) ---


def build_default_registry() -> ModuleRegistry:
    """
    Build default module registry with bundled adapters.
    """
    registry = ModuleRegistry()
    registry.register(PassiveDNSAdapter)
    registry.register(WhoisRDAPAdapter)
    registry.register(TLSInfoAdapter)
    return registry
