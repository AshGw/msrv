import concurrent.futures
import multiprocessing
import threading
from functools import wraps
from typing import Any, Callable, List, Optional

from app.lib.funcs.cpu_watch import max_cpu_cores


class Executioner:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def processor(funcs: List[Callable], join: Optional[bool] = False):
        def decorator(func: Any):
            @wraps(func)
            def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
                processes = [multiprocessing.Process(target=f) for f in funcs]
                for process in processes:
                    process.start()
                if join:
                    for process in processes:
                        process.join()

                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def thread(fn: Any):
        def execute(*k: tuple[Any, ...], **kw: dict[str, Any]) -> Any:
            f = threading.Thread(target=fn, args=k, kwargs=kw)
            f.start()
            return f

        return execute

    # Both above are meant to be used as @decorators
    @staticmethod
    def cores_limited_multiprocessor(
        callables: List[Callable], max_workers: int = max_cpu_cores()
    ) -> None:
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=max_workers
        ) as executor:
            futures = [executor.submit(callable_func) for callable_func in callables]
            concurrent.futures.wait(futures)

    # After trial this turns out to be the safest option to not overload the server
    # Tho executioner is the most optimal


"""
@Executioner.concurrent(callables, join=True)
    def run_in_parallel_holder():
        pass

    def parallel_exec():
        run_in_parallel_holder()
"""
