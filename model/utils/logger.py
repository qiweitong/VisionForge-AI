import logging
import os

def get_logger(log_dir):

    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("VisionForge")

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(
        os.path.join(log_dir, "train.log"),
        encoding="utf-8"
    )

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger