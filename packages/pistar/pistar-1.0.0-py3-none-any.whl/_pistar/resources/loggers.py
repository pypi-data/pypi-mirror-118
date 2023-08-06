import logging
import colorlog
from _pistar.utilities.constants import LOGGING_LEVEL


class ServerLogger(logging.Logger):
    """
    description: this class is the logger of gtr python.
    """

    __level = None
    __format = None
    __colors = None

    def __init__(self, name, level=LOGGING_LEVEL.DEBUG, logger_format=None):
        super().__init__(name)

        self.__format = logger_format
        self.__level = level
        self.__colors = {
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }

        self.__create_stream_handler()

    def __create_stream_handler(self):
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s' + self.__format,
            log_colors=self.__colors
        )

        sh = logging.StreamHandler()
        sh.setLevel(self.__level)
        sh.setFormatter(formatter)
        self.addHandler(sh)

    def close(self):
        """
        description: this function is used to
                     close the file handler of the logger.
        """

        for handler in self.handlers:
            handler.close()
            self.removeHandler(handler)

    def __delete_handlers(self, types):
        for handler in self.handlers:
            if not isinstance(handler, types):
                continue
            self.removeHandler(handler)


server_logger = ServerLogger(
    name='server_logger',
    level=LOGGING_LEVEL.DEBUG,
    logger_format='[%(asctime)s] [%(levelname)s] [%(name)s] [%(pathname)s:%(lineno)d] %(message)s'
)
