import win32com.client

# import application utils here
from .app_utils.version import Version
from .app_utils.ui import Ui

class Application:
    def __init__(self) -> None:
        self.com_obj = win32com.client.Dispatch('CANalyzer.Application')

    def bus(self, type="CAN"):
        return self.com_obj.Bus(type)

    @property
    def capl(self):
        return self.com_obj.CAPL

    @property
    def channel_mapping_name(self):
        return self.com_obj.ChannelMappingName

    @channel_mapping_name.setter
    def channel_mapping_name(self, name: str):
        self.com_obj.ChannelMappingName = name

    @property
    def configuration(self):
        return self.com_obj.Configuration

    @property
    def full_name(self):
        return self.com_obj.FullName

    @property
    def measurement(self):
        return self.com_obj.Measurement

    @property
    def name(self):
        return self.com_obj.Name

    @property
    def networks(self):
        return self.com_obj.Networks()

    @property
    def path(self):
        return self.com_obj.Path

    @property
    def system(self):
        return self.com_obj.System

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
