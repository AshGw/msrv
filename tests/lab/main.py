from typing import Any


def check_env_var(attr_name: str, attr_value: Any) -> None:
    if attr_value is None:
        raise ValueError(f"Environment variable for: {attr_name} does not exist!")
