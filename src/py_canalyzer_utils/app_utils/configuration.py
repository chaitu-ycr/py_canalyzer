# Import Python Libraries here
import logging
import pythoncom
import win32com.client
from time import sleep as wait

logger_inst = logging.getLogger('CANALYZER_LOG')


class CanalyzerConfigurationEvents:
    """Handler for CANalyzer Configuration events"""

    @staticmethod
    def OnClose():
        """Occurs when the configuration is closed.
        """
        logger_inst.info('configuration OnClose event triggered.')

    @staticmethod
    def OnSystemVariablesDefinitionChanged():
        """Occurs when system variable definitions are added, changed or removed.
        """
        logger_inst.info('configuration OnSystemVariablesDefinitionChanged event triggered.')


class Configuration:
    """The Configuration object represents the active configuration.
    """

    def __init__(self, app_com_obj, enable_config_events=False):
        """The Configuration object init method.

        Args:
            app_com_obj (_type_): application com object.
            enable_config_events (bool, optional): option to enable config events. Defaults to False.
        """
        self.log = logger_inst
        self.com_obj = win32com.client.Dispatch(app_com_obj.Configuration)
        if enable_config_events:
            win32com.client.WithEvents(self.com_obj, CanalyzerConfigurationEvents)

    @property
    def comment(self) -> str:
        """Gets the comment for the configuration.

        Returns:
            str: The comment.
        """
        return self.com_obj.Comment

    @comment.setter
    def comment(self, text: str) -> None:
        """Defines the comment for the configuration.

        Args:
            text (str): The comment.
        """
        self.com_obj.Comment = text
        self.log.info(f'configuration comment set to {text}.')

    @property
    def full_name(self) -> str:
        """gets the complete path of the configuration.

        Returns:
            str: complete path of the configuration.
        """
        return self.com_obj.FullName

    @full_name.setter
    def full_name(self, full_name: str):
        """sets the complete path of the configuration.

        Args:
            full_name (str): The new complete path of the configuration.
        """
        self.com_obj.FullName = full_name
        self.log.info(f'complete path of the configuration set to {full_name}.')

    @property
    def mode(self) -> int:
        """returns whether the Online mode or the Offline mode is active.

        Returns:
            int: The currently active mode.
        """
        return self.com_obj.Mode

    @mode.setter
    def mode(self, mode: int) -> None:
        """sets the Online mode or the Offline mode to active.

        Args:
            mode (int): The active mode; valid values are: 0-Online mode is activated. 1-Offline mode is activated.
        """
        self.com_obj.Mode = mode
        self.log.info(f'offline/online mode set to {mode}.')

    @property
    def modified(self) -> bool:
        """Returns information on whether the current configuration was modified since the time it was loaded or created, or sets this property.
        This property determines whether the user is prompted to save when another configuration is loaded.

        Returns:
            bool: The current value of the property.
        """
        return self.com_obj.Modified

    @modified.setter
    def modified(self, modified: bool) -> None:
        """sets Modified property to false/true.

        Args:
            modified (bool): Value to be assigned to the Modified property.
        """
        self.com_obj.Modified = modified
        self.log.info(f'configuration modified property set to {modified}.')

    @property
    def name(self) -> str:
        """Returns the name of the configuration.

        Returns:
            str: The name of the currently loaded configuration.
        """
        return self.com_obj.Name

    @property
    def path(self) -> str:
        """returns the path of the configuration, depending on the actual configuration.

        Returns:
            str: The path of the currently loaded configuration.
        """
        return self.com_obj.Path

    @property
    def read_only(self) -> bool:
        """Indicates whether the configuration is write protected.

        Returns:
            bool: If the object is write protected True is returned; otherwise False is returned.
        """
        return self.com_obj.ReadOnly

    @property
    def saved(self) -> bool:
        """Indicates whether changes to the configuration have already been saved.

        Returns:
            bool: False is returned, If changes were made to the configuration and not been saved yet. otherwise True is returned.
        """
        return self.com_obj.Saved

    def save(self, path='', prompt_user=False):
        """Saves the configuration.

        Args:
            path (str): The complete file name. If no path is specified, the configuration is saved under its current name. If it is not saved yet, the user will be prompted for a name.
            prompt_user (bool, optional): A boolean value that indicates whether the user should intervene in error situations.
        """
        if not self.saved:
            if path == '':
                self.com_obj.Save()
            else:
                self.com_obj.Save(path, prompt_user)
            self.log.info(f'Saved configuration({path}).')
        else:
            self.log.info('CANalyzer Configuration already in saved state.')
        return self.saved

    def save_as(self, path: str, major: int, minor: int, prompt_user: bool):
        """Saves the configuration as a different CANalyzer version

        Args:
            path (str): The complete path.
            major (int): The major version number of the target version, e.g. 10 for CANalyzer 10.1.
            minor (int): The minor version number of the target version, e.g. 1 for CANalyzer 10.1
            prompt_user (bool): A boolean value that defines whether the user should interact in error situations.
        """
        self.com_obj.SaveAs(path, major, minor, prompt_user)
        self.log.info(f'Saved configuration as {path}.')
