"""Python package for controlling Vector CANalyzer tool"""

# Import Python Libraries here
import os
import pythoncom
from typing import Union
from time import sleep as wait

# import CANalyzer utils here
from py_canalyzer_utils.py_logger import PyLogger
from py_canalyzer_utils.application import Application

class CANalyzer:
    r"""The CANalyzer class represents the CANalyzer application.
    The CANalyzer class is the foundation for the object hierarchy.
    You can reach all other methods from the CANalyzer class instance.

    Examples:
        >>> # Example to open CANalyzer configuration, start measurement, stop measurement and close configuration.
        >>> canalyzer_inst = CANalyzer(py_canalyzer_log_dir=r'D:\.py_canalyzer')
        >>> canalyzer_inst.open(r'D:\py_canalyzer\demo_cfg\demo.cfg')
        >>> canalyzer_inst.start_measurement()
        >>> wait(10)
        >>> canalyzer_inst.stop_measurement()
        >>> canalyzer_inst.quit()
    """
    def __init__(self, py_log_dir='') -> None:
        pcl = PyLogger(py_log_dir)
        self.log = pcl.log
        self.application: Application

    def open(self, canalyzer_cfg: str, visible=True, auto_save=False, prompt_user=False) -> None:
        r"""Loads CANalyzer configuration.

        Args:
            canalyzer_cfg (str): The complete path for the CANalyzer configuration.
            visible (bool): True if you want to see CANalyzer UI. Defaults to True.
            auto_save (bool, optional): A boolean value that indicates whether the active configuration should be saved if it has been changed. Defaults to False.
            prompt_user (bool, optional): A boolean value that indicates whether the user should intervene in error situations. Defaults to False.
        """
        pythoncom.CoInitialize()
        self.application = Application()
        self.application.visible = visible
        self.application.open(path=canalyzer_cfg, auto_save=auto_save, prompt_user=prompt_user)
