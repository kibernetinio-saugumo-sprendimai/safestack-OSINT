from abc import ABC, abstractmethod
from core_control.context import Context
from core_control.result import Result


class ModuleContract(ABC):
    """
    Base contract for all OSINT modules.

    A module is a PURE execution unit:
    - no printing
    - no process control
    - no global state mutation
    """

    #: Unique module identifier (e.g. dns.passive)
    name: str

    def validate(self, context: Context) -> None:
        """
        Optional pre-run validation hook.

        May raise an exception if execution should not proceed.
        Default: no validation.
        """
        return None

    @abstractmethod
    def run(self, context: Context) -> Result:
        """
        Execute module logic.

        MUST:
        - accept Context
        - return Result
        - raise controlled exceptions on failure
        """
        raise NotImplementedError
