# Module Development

SafeStack OSINT uses an **Adapter Pattern** to wrap individual OSINT tools into a standardized framework.

## 🏗️ Architecture

1. **Module (`modules/`)**: The core logic (e.g., DNS resolver, API client).
2. **Adapter (`adapters/`)**: Implements `ModuleContract` and maps the core logic to the framework's `Result` type.
3. **Registry (`core_control/registry.py`)**: Registers the adapter for use in the CLI.

## 📝 Creating a New Module

### 1. Implement the Core Logic
Create a class in `modules/my_module/module.py`. It should return a dictionary.

```python
class MyModule:
    def run(self, target: str):
        return {"data": "...", "source": "my_api"}
```

### 2. Create the Adapter
Create `adapters/my_module/adapter.py`.

```python
from core_control.module_contract import ModuleContract
from core_control.result import Result

class MyModuleAdapter(ModuleContract):
    name = "my.module"

    def run(self, context):
        from modules.my_module.module import MyModule
        raw = MyModule().run(context.target)
        
        return Result(
            module=self.name,
            target=context.target,
            data=raw,
            confidence=0.9,
            sources=["my_api"]
        )
```

### 3. Register the Adapter
In `core_control/registry.py`, import and register your adapter in `build_default_registry()`:

```python
from adapters.my_module.adapter import MyModuleAdapter
# ...
registry.register(MyModuleAdapter)
```

## 📜 Module Contract Rules

- **Pure Execution**: Modules should not print to `stdout`.
- **Stateless**: Modules should not depend on global state.
- **Context Awareness**: Use the `context` object for mode-specific behavior.
