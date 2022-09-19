from logging import getLogger, Logger, DEBUG, StreamHandler, Formatter


def get_formatter() -> Formatter:
    formatter = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return formatter


def get_stream_handler() -> StreamHandler:
    handler = StreamHandler()
    formatter = get_formatter()
    handler.setFormatter(formatter)
    return handler


def get_logger() -> Logger:
    logger_obj = getLogger(__name__)
    logger_obj.setLevel(DEBUG)
    stream_handler = get_stream_handler()
    logger_obj.addHandler(stream_handler)
    return logger_obj


logger = get_logger()
