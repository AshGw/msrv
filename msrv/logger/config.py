import logging

from msrv.logger._consts import FileModes, Format, Names


def setup_logging(
    *,
    log_level: int,
    log_format: str,
    date_format: str,
    use_remote: bool,
    filename: str,
    filemode: str,
):
    log_format = log_format
    date_format = date_format
    logging.basicConfig(
        level=log_level,
        filename=filename,
        format=log_format,
        filemode=filemode,
    )
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)

    if use_remote:
        # TODO: Add additional handlers or configurations as needed
        pass


setup_logging(
    log_level=logging.INFO,
    log_format=Format.LOG,
    date_format=Format.DATE,
    filename=Names.LOG_FILENAME,
    filemode=FileModes.APPEND,
    use_remote=False,
)
