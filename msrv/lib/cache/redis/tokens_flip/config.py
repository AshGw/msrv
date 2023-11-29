from enum import Enum


class RedisConf(Enum):
    """
    a switch, if false then the msrv uses 3rd party remote Redis instances,
    else it uses local spun up Docker containers
    """

    use_local = False
