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
    def __init__(self, user_capl_function_names: tuple):
        self.user_capl_function_names = user_capl_function_names
        self.com_obj = win32com.client.Dispatch('CANalyzer.Application')

    def bus(self, type="CAN"):
        return Bus(self.com_obj, type)

    @property
    def capl(self):
        return Capl(self.com_obj)

    @property
    def channel_mapping_name(self):
        return self.com_obj.ChannelMappingName

    @channel_mapping_name.setter
    def channel_mapping_name(self, name: str):
        self.com_obj.ChannelMappingName = name

    @property
    def configuration(self):
        return Configuration(self.com_obj)

    @property
    def full_name(self):
        return self.com_obj.FullName

    @property
    def measurement(self):
        return Measurement(self.com_obj, self.user_capl_function_names)

    @property
    def name(self):
        return self.com_obj.Name

    @property
    def networks(self):
        return Networks(self.com_obj)

    @property
    def path(self):
        return self.com_obj.Path

    @property
    def performance(self):
        return Performance(self.com_obj)

    @property
    def system(self):
        return System(self.com_obj)

    @property
    def ui(self):
        return Ui(self.com_obj)

    @property
    def version(self):
        return Version(self.com_obj)

    @property
    def visible(self):
        return self.com_obj.Visible

    @visible.setter
    def visible(self, value=True):
        self.com_obj.Visible = value

    def new(self, autosave=True, prompt_user=False):
        self.com_obj.New(autosave, prompt_user)

    def open(self, path: str, autosave=True, prompt_user=False):
        self.com_obj.Open(path, autosave, prompt_user)

    def quit(self):
        self.com_obj.Quit()
