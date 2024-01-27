# Import Python Libraries here
import os
import sys
import logging
from logging import handlers


class PyLogger:
    def __init__(self, py_log_dir='') -> None:
        self.log = logging.getLogger('CANalyzer_LOG')
        self.log.handlers.clear()
        self.log.propagate = False
        self.__py_log_initialization(py_log_dir)

    def __py_log_initialization(self, py_log_dir):
        self.log.setLevel(logging.DEBUG)
        log_format = logging.Formatter("%(asctime)s [CANALYZER_LOG] [%(levelname)-5.5s] %(message)s")
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(log_format)
        self.log.addHandler(ch)
        if py_log_dir != '' and not os.path.exists(py_log_dir):
            os.makedirs(py_log_dir, exist_ok=True)
        if os.path.exists(py_log_dir):
            fh = handlers.RotatingFileHandler(fr'{py_log_dir}\py_canalyzer.log', maxBytes=0)
            fh.setFormatter(log_format)
            self.log.addHandler(fh)
