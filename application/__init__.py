import logging
import time

from .config import get_config
from .excel import excel
from .load_data import load_data
from .project_parser import parser

logging.basicConfig(level='INFO', format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
logger = logging.getLogger(__package__)

__version__ = '0.0.1'


def main():
    start_time = time.time()
    logger.info(f'Start program')
    logger.debug(f'Version: {__version__}')
    try:
        conf = get_config()
        issues = parser(conf)
        data = load_data(issues, conf)
        excel(data)
    except Exception as error:
        logger.error(error)
        exit(-1)
    else:
        logger.info(f'End program: time: {round(time.time() - start_time, 2)}s')
