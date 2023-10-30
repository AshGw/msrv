import csv
from datetime import datetime


def current_time() -> str:
    return datetime.now().isoformat()


def logging_service(
    message: str, time: str = current_time(), *, service="csv", **kwargs
):
    if service == "csv":
        filename = kwargs.get("filename", "logger.csv")
        with open(f"{filename}", mode="a", newline="") as logger:
            writer = csv.writer(
                logger, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow([time, message, service])

    # Implement an actual logging service logic here
    pass
