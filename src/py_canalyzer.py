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
    """

    def __init__(self, py_log_dir='') -> None:
        pcl = PyLogger(py_log_dir)
        self.log = pcl.log
        self.app_obj = Application

    def get_application_info(self) -> str:
        """Vector CANalyzer Application Version.

        Returns:
            str: return Vector CANalyzer Application Version. "major.minor.build" -> "12.01.04"
        """
        cav = self.app_obj.version
        app_version = f"{cav.major}.{cav.minor}.{cav.build}"
        self.log.info(f'Vector CANalyzer Application Version -> {app_version}')
        return app_version

    def open(self, canalyzer_cfg: str, visible=True, auto_save=False, prompt_user=False) -> None:
        r"""Loads CANalyzer configuration.

        Args:
            canalyzer_cfg (str): The complete path for the CANalyzer configuration.
            visible (bool): True if you want to see CANalyzer UI. Defaults to True.
            auto_save (bool, optional): A boolean value that indicates whether the active configuration should be saved if it has been changed. Defaults to False.
            prompt_user (bool, optional): A boolean value that indicates whether the user should intervene in error situations. Defaults to False.

        Raises:
            FileNotFoundError: error when CANalyzer config file not available in pc.
        """
        pythoncom.CoInitialize()
        self.app_obj = Application()
        if not auto_save:
            self.app_obj.configuration.Modified = False
            self.log.info(f'CANalyzer cfg "Modified" parameter set to False to avoid error.')
        if os.path.isfile(canalyzer_cfg):
            self.log.info(f'CANalyzer cfg "{canalyzer_cfg}" found.')
            self.app_obj.visible = visible
            self.app_obj.open(canalyzer_cfg, auto_save, prompt_user)
            self.log.info(f'loaded CANalyzer config "{canalyzer_cfg}"')
            self.get_application_info()
        else:
            self.log.info(f'CANalyzer cfg "{canalyzer_cfg}" not found.')
            raise FileNotFoundError(f'CANalyzer cfg file "{canalyzer_cfg}" not found!')

    def quit(self):
        """Quits the application.
        """
        self.app_obj.quit()
        self.log.info('CANalyzer Application Closed.')
