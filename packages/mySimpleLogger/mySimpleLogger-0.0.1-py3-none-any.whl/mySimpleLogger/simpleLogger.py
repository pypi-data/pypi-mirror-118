import logging
import sys

_fileHandler = logging.FileHandler("log.txt")
_soutHandler = logging.StreamHandler(sys.stdout)

_logFormatStr='%(asctime)s - %(levelname)s %(name)s [%(threadName)s] %(filename)s:%(lineno)d %(funcName)s  - %(message)s'
logging.basicConfig(level = logging.INFO,format = _logFormatStr,handlers=[_fileHandler,_soutHandler])


logger = logging.getLogger()


def filterOutZFSpaceHeaderWarn():
    '''
    space in header name not support by python, and not fit the standard too，will print warn and stop parse headers after
    '''
    class ignoreHeaderFilter(logging.Filter):
        def filter(self, record: logging.LogRecord):
            return not 'who am i: coder zf' in record.getMessage()

    logging.getLogger('urllib3.connectionpool').addFilter(ignoreHeaderFilter())


if __name__ == '__main__':
    logger.info('logger info')
    logger.debug('logger debug')
    logger.warning('logger warn')
    try:
        raise Exception("test Exception")
    except Exception as e:
        logger.warning("got exception", exc_info=True)
    logger.info("after out put exception")
    logger.info(1)
else:
    #just ensure that import will only run once
    logger.info('loaded logger as model %s',__name__)