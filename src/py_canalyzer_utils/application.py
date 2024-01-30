import win32com.client

# import application utils here
from .app_utils.bus import Bus
from .app_utils.capl import Capl
from .app_utils.configuration import Configuration
from .app_utils.measurement import Measurement
from .app_utils.networks import Networks
from .app_utils.performance import Performance
from .app_utils.system import System
from .app_utils.ui import Ui
from .app_utils.version import Version


class Application:
    """The Application object represents the CANalyzer application.
    """
    def __init__(self, user_capl_function_names: tuple):
        self.user_capl_function_names = user_capl_function_names
        self.com_obj = win32com.client.Dispatch('CANalyzer.Application')
        self.bus = Bus
        self.capl = Capl
        self.configuration = Configuration
        self.measurement = Measurement
        self.networks = Networks
        self.performance = Performance
        self.system = System
        self.ui = Ui
        self.version = Version

    @property
    def channel_mapping_name(self) -> str:
        """get the application name which is used to map application channels to real existing Vector hardware interface channels.

        Returns:
            str: The application name
        """
        return self.com_obj.ChannelMappingName

    @channel_mapping_name.setter
    def channel_mapping_name(self, name: str):
        """set the application name which is used to map application channels to real existing Vector hardware interface channels.

        Args:
            name (str): The application name used to map the channels.
        """
        self.com_obj.ChannelMappingName = name

    @property
    def full_name(self) -> str:
        """determines the complete path of the CANalyzer application.

        Returns:
            str: location where CANalyzer is installed.
        """
        return self.com_obj.FullName

    @property
    def name(self) -> str:
        """Returns the name of the CANalyzer application.

        Returns:
            str: name of the CANalyzer application.
        """
        return self.com_obj.Name

    @property
    def path(self) -> str:
        """Returns the Path of the CANalyzer application.

        Returns:
            str: Path of the CANalyzer application.
        """
        return self.com_obj.Path

    @property
    def visible(self) -> bool:
        """Returns whether the CANalyzer main window is visible or is only displayed by a tray icon.

        Returns:
            bool: A boolean value indicating whether the CANalyzer main window is visible..
        """
        return self.com_obj.Visible

    @visible.setter
    def visible(self, visible: bool):
        """Defines whether the CANalyzer main window is visible or is only displayed by a tray icon.

        Args:
            visible (bool): A boolean value indicating whether the CANalyzer main window is to be visible.
        """
        self.com_obj.Visible = visible

    def new(self, auto_save=False, prompt_user=False) -> None:
        """Creates a new configuration.

        Args:
            auto_save (bool, optional): A boolean value that indicates whether the active configuration should be saved if it has been changed. Defaults to False.
            prompt_user (bool, optional): A boolean value that indicates whether the user should intervene in error situations. Defaults to False.
        """
        self.com_obj.New(auto_save, prompt_user)

    def open(self, path: str, auto_save=False, prompt_user=False) -> None:
        """Loads a configuration.

        Args:
            path (str): The complete path for the configuration.
            auto_save (bool, optional): A boolean value that indicates whether the active configuration should be saved if it has been changed. Defaults to False.
            prompt_user (bool, optional): A boolean value that indicates whether the user should intervene in error situations. Defaults to False.
        """
        self.com_obj.Open(path, auto_save, prompt_user)
        self.bus = Bus(self.com_obj)
        self.capl = Capl(self.com_obj)
        self.configuration = Configuration(self.com_obj)
        self.networks = Networks(self.com_obj)
        self.performance = Performance(self.com_obj)
        self.system = System(self.com_obj)
        self.ui = Ui(self.com_obj)
        self.version = Version(self.com_obj)
        self.measurement = Measurement(self.com_obj, self.user_capl_function_names)

    def quit(self):
        """Quits the application.
        """
        self.com_obj.Quit()
