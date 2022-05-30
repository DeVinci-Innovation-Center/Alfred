import logging


def config_logger(logger_name: str):
    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        fmt="{asctime} - {name} - {levelname: <8} - {message}",
        datefmt="%d-%m-%Y %H:%M:%S",
        style="{",  # noqa: E501
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    # 'application' code
    # logger.debug("debug message")
    # logger.info("info message")
    # logger.warning("warn message")
    # logger.error("error message")
    # logger.critical("critical message")
