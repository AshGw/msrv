import multiprocessing
import os

import psutil
from dotenv import load_dotenv
from starlette.exceptions import HTTPException

from app.lib.logger.main import logging_service

load_dotenv()


def server_overloaded():
    cpu_usage = psutil.cpu_percent(interval=1)

    if cpu_usage > 95:
        return True
    else:
        return False


def overload_check():
    if (
        server_overloaded()
    ):  # Allow mfs to bombard this endpoint so u adjust the threshold as needed
        logging_service(message="THE SERVER IS OVERLOADED!!")
        raise HTTPException(detail="Server overloaded", status_code=529)


def max_cpu_cores() -> int:
    try:
        return os.cpu_count() or multiprocessing.cpu_count()
    except (AttributeError, NotImplementedError):
        return int(os.getenv("FALLBACK_HOST_MACHINE_CPU_CORES"))
        # TODO THIS WILL NEED FURTHER ANALYSIS DEPENDING ON THE CLOUD INSTANCE
