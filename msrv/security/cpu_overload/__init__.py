from multiprocessing import cpu_count as mp_cpu_count
from os import cpu_count as os_cpu_count
from psutil import cpu_percent
from starlette.exceptions import HTTPException
from msrv.lib.env import Env
from msrv.logger import logging


def server_overloaded() -> bool:
    cpu_usage = cpu_percent(interval=1)

    if cpu_usage > 98:
        return True
    else:
        return False


def overload_check() -> None:
    if (
        server_overloaded()
    ):  # Allow mfs to bombard this endpoint so u adjust the threshold as needed
        logging.critical("THE SERVER IS OVERLOADED!!")
        raise HTTPException(detail="Server overloaded", status_code=529)


def max_cpu_cores() -> int:
    try:
        return os_cpu_count() or mp_cpu_count()
    except (AttributeError, NotImplementedError):
        return int(Env.Public.FALLBACK_HOST_MACHINE_CPU_CORES)
        # TODO THIS WILL NEED FURTHER ANALYSIS DEPENDING ON THE CLOUD INSTANCE
