import json
import logging.config
import os


def load_logger_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config


def debug(*args):
    if len(args) == 1:
        logger.debug(str(args[0]))
    else:
        logger.debug(' '.join([str(i) for i in args]))


def info(*args):
    if len(args) == 1:
        logger.info(str(args[0]))
    else:
        logger.info(' '.join([str(i) for i in args]))


def warning(*args):
    if len(args) == 1:
        logger.warning(str(args[0]))
    else:
        logger.warning(' '.join([str(i) for i in args]))


def exception(e):
    logger.exception(e, exc_info=True)


def critical(*args):
    if len(args) == 1:
        logger.critical(str(args[0]))
    else:
        logger.critical(' '.join([str(i) for i in args]))


config_filename = os.getcwd()+"/app/utils/logger/logging_config.json"
LOGGER_CONFIG = load_logger_config(config_filename)

# configuring logger from dictionary
logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)

debug('Logger Configuration', 'Successful')
