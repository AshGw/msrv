class Names:
    LOG_FILENAME = "logger.log"


class LogMethod:
    CONSOLE: str = "console"
    FILE: str = "file"


class FileModes:
    APPEND: str = "a"
    WRITE: str = "w"


class Format:
    LOG: str = (
        "%(asctime)s - %(levelname)s - %(message)s (Line: %(lineno)d [%(filename)s])"
    )
    DATE: str = "%Y-%m-%d %I:%M:%S %p"
