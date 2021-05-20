import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger("stackoverflow-dashboard-backend-etl")
    logger.setLevel(logging.INFO)
    return logger
