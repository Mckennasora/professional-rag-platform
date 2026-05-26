import logging


def configure_logging() -> None:
    # TODO: Replace with structured logging when the service grows.
    logging.basicConfig(level=logging.INFO)
