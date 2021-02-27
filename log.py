import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='debug.log', format=log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def print_and_log(msg):
    print(msg)
    logger.info(msg)
