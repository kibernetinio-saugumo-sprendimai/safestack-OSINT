class CoreControlError(Exception):
    """
    Base exception for all core_control errors.
    """
    pass


class ModuleExecutionError(CoreControlError):
    """
    Raised when a module fails during execution.
    """
    pass


class PolicyViolationError(CoreControlError):
    """
    Raised when a module violates execution policy.
    """
    pass
