import logging


def setup_logger(name: str):
    logger = logging.getLogger(name)

    logging_format = logging.Formatter(
        '%(asctime)s~%(levelname)s~\t%(message)s\n\t ~module:%(module)s\n\t~function:%(module)s'
        )
    stdout_formating = logging.Formatter('%(levelname)s - %(message)s')

    file_handler = logging.FileHandler(f"/tmp/{name}.log")
    file_handler.setFormatter(stdout_formating)
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stdout_formating)
    stream_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger
