import logging
import logging.handlers
from logging import *
import traceback


LOG_FILENAME = 'main.log'
LOG_LEVEL = ERROR


class MyLogger(Logger):

    def __init__(self, name, level=NOTSET):
        super(MyLogger, self).__init__(name=name, level=level)

    def _log(
            self,
            level,
            msg,
            args,
            exc_info=None,
            extra=None,
            stack_info=False,
            robot=False
    ) -> None:
        """

        :param level:
        :param msg:
        :param args:
        :param exc_info:
        :param extra:
        :param stack_info:
        :return:
        """
        if level >= LOG_LEVEL:
            msg += '\n' + traceback.format_exc()
        super(MyLogger, self)._log(level, msg, args, exc_info, extra, stack_info)


    def __reduce__(self):
        return getLogger, ()


logger = MyLogger('tweetScraper', WARNING)


def set_logger():
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                                  '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()
