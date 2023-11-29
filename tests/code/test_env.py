import unittest

from msrv.lib.env import Env

from ..lab import check_env_var


def test__dev__():
    for attr_name, attr_value in Env.Dev.__dict__.items():
        if (
            not attr_name.startswith("__")
            and attr_value is not None
            and not isinstance(attr_value, type)
        ):
            check_env_var(attr_name, attr_value)


def test__dev_origins__():
    for attr_name, attr_value in Env.Dev.Origins.__dict__.items():
        if not attr_name.startswith("__") and not isinstance(attr_value, type):
            check_env_var(attr_name, attr_value)


def test__prod__():
    for attr_name, attr_value in Env.Prod.__dict__.items():
        if (
            not attr_name.startswith("__")
            and attr_value is not None
            and not isinstance(attr_value, type)
        ):
            check_env_var(attr_name, attr_value)


def test__prod_hf__():
    for attr_name, attr_value in Env.Prod.HF.__dict__.items():
        if not attr_name.startswith("__") and not isinstance(attr_value, type):
            check_env_var(attr_name, attr_value)


def test__prod_hf_keys_exec__():
    for attr_name, attr_value in Env.Prod.HF.KEYS.ExecTokens.__dict__.items():
        if not attr_name.startswith("__") and not isinstance(attr_value, type):
            check_env_var(attr_name, attr_value)


def test__prod_hf_keys_personal__():
    for attr_name, attr_value in Env.Prod.HF.KEYS.Personal.__dict__.items():
        if not attr_name.startswith("__") and not isinstance(attr_value, type):
            check_env_var(attr_name, attr_value)


def test__prod_redis_tokencacher__():
    for attr_name, attr_value in Env.Prod.Redis.TokensCache.__dict__.items():
        if not attr_name.startswith("__") and not isinstance(attr_value, type):
            check_env_var(attr_name, attr_value)


def test__prod_redis_rate_limits_cacher__():
    for attr_name, attr_value in Env.Prod.Redis.RateLimitsCache.__dict__.items():
        if not attr_name.startswith("__") and not isinstance(attr_value, type):
            check_env_var(attr_name, attr_value)


def test__public__():
    for attr_name, attr_value in Env.Public.__dict__.items():
        if not attr_name.startswith("__") and not isinstance(attr_value, type):
            check_env_var(attr_name, attr_value)


def test__current_env__():
    for attr_name, attr_value in Env.__dict__.items():
        if not attr_name.startswith("__") and not isinstance(attr_value, type):
            check_env_var(attr_name, attr_value)


if __name__ == "__main__":
    unittest.main()
