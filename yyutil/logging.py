# -*- coding: utf-8 -*-
import logging

TRACE = 5

logging.addLevelName(logging.FATAL, "FATAL")
logging.addLevelName(logging.WARN, "WARN")
logging.addLevelName(TRACE, "TRACE")


def _trace(self, msg, *args, **kwargs):
    self.log(TRACE, msg, *args, **kwargs)


logging.Logger.trace = _trace


class ColorfulFormatter(logging.Formatter):
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)

    COLOR_CODE = "\033[1;%dm"
    RESET_CODE = "\033[0m"

    NAME_CODE = COLOR_CODE % CYAN

    LEVEL_COLOR = {
        "FATAL": COLOR_CODE % RED,
        "ERROR": COLOR_CODE % RED,
        "WARN": COLOR_CODE % YELLOW,
        "INFO": COLOR_CODE % BLUE,
        "DEBUG": COLOR_CODE % MAGENTA,
        "TRACE": COLOR_CODE % WHITE
    }

    def format(self, record):
        # record = self.reset_levelname(record)

        color = self.LEVEL_COLOR.get(record.levelname)
        if color:
            record.levelname = color + record.levelname + self.RESET_CODE

        record.name = self.NAME_CODE + record.name + self.RESET_CODE

        return super().format(record)
