# Import Python Libraries here
import logging
import os
import win32com.client


class Application:
    """The Application object represents the CANalyzer application.
    """

    def __init__(self):
        self.log = logging.getLogger('CANALYZER_LOG')
        self.com_obj = win32com.client.Dispatch('CANalyzer.Application')
        self.__print_application_info()

    def __print_application_info(self):
        cav = self.com_obj.Version
        self.log.info(f'Dispatched Vector CANalyzer Application {cav.major}.{cav.minor}.{cav.Build}')

    def open(self, path: str, auto_save=False, prompt_user=False) -> None:
        """Loads a configuration.

        Args:
            path (str): The complete path for the configuration.
            auto_save (bool, optional): A boolean value that indicates whether the active configuration should be saved if it has been changed. Defaults to False.
            prompt_user (bool, optional): A boolean value that indicates whether the user should intervene in error situations. Defaults to False.

        Raises:
            FileNotFoundError: error when CANalyzer config file not available in pc.
        """
        if not auto_save:
            self.com_obj.Configuration.Modified = False
            self.log.info(f'CANalyzer cfg "Modified" parameter set to False to avoid error.')
        if os.path.isfile(path):
            self.log.info(f'CANalyzer cfg "{path}" found.')
            self.com_obj.Open(path, auto_save, prompt_user)
            self.log.info(f'loaded CANalyzer config "{path}"')

        else:
            self.log.info(f'CANalyzer cfg "{path}" not found.')
            raise FileNotFoundError(f'CANalyzer cfg file "{path}" not found!')

    def quit(self):
        """Quits the application.
        """
        self.com_obj.Quit()
        self.log.info('CANalyzer Application Closed.')
