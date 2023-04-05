import logging
from cowsim.utils.color import FORES, BRIGHTNESS, color_string


class LogFormatter(logging.Formatter):
    # Set format
    debug_format = "%(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    info_format = "%(levelname)s - %(message)s"
    error_format = "%(levelname)s - %(message)s"
    FORMATS = {
        logging.DEBUG: color_string(debug_format, FORES["green"], BRIGHTNESS["dim"]),
        logging.INFO: color_string(info_format, FORES["green"]),
        logging.WARNING: color_string(info_format, FORES["yellow"]),
        logging.ERROR: color_string(error_format, FORES["red"]),
        logging.FATAL: color_string(error_format, FORES["red"], BRIGHTNESS["bright"]),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def instantiate_logger(app_name=""):
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(LogFormatter())

    logger.addHandler(ch)
    return logger


LOG = instantiate_logger("Cowsim")
