import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger("stackoverflow-dashboard-backend")
    logger.setLevel(logging.INFO)
    return logger
