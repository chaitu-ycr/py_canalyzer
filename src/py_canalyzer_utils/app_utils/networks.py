# Import Python Libraries here
import logging
import pythoncom
import win32com.client
from time import sleep as wait


class Networks:
    """The Networks class represents the networks of CANalyzer.
    """
    def __init__(self, app_com_obj):
        self.log = logging.getLogger('CANALYZER_LOG')
        self.com_obj = win32com.client.Dispatch(app_com_obj.Networks)

    @property
    def count(self) -> int:
        """Returns the number of Networks inside the collection.

        Returns:
            int: The number of Networks contained
        """
        return self.com_obj.Count

    def fetch_all_networks(self) -> dict:
        """returns all networks available in configuration.
        """
        networks = dict()
        for index in range(1, self.count + 1):
            network_com_obj = win32com.client.Dispatch(self.com_obj.Item(index))
            network = Network(network_com_obj)
            networks[network_com_obj.Name] = network
        return networks

    def fetch_all_diag_devices(self) -> dict:
        """returns all diagnostic devices available in configuration.
        """
        diag_devices = dict()
        networks = self.fetch_all_networks()
        if len(networks) > 0:
            for _, n_value in networks.items():
                devices = n_value.devices
                n_devices = devices.get_all_devices()
                if len(n_devices) > 0:
                    for d_name, d_value in n_devices.items():
                        if d_value.diagnostic is not None:
                            diag_devices[d_name] = d_value.diagnostic
        return diag_devices


class Network:
    """The Network class represents one single network of CANalyzer.
    """
    def __init__(self, network_com_obj):
        self.com_obj = network_com_obj

    @property
    def bus_type(self) -> int:
        """Determines the bus type of the network

        Returns:
            int: The type of the network: 0-Invalid, 1-CAN, 2-J1939, 5-LIN, 6-MOST, 7-FlexRay, 9-J1708, 11-Ethernet
        """
        return self.com_obj.BusType

    @property
    def devices(self) -> object:
        """Returns the Devices class.

        Returns:
            object: The Devices object
        """
        return Devices(self.com_obj)

    @property
    def name(self) -> str:
        """The name of the network.
        """
        return self.com_obj.Name


class Devices:
    """The Devices class represents all devices of CANalyzer.
    """
    def __init__(self, network_com_obj):
        self.com_obj = network_com_obj.Devices

    @property
    def count(self) -> int:
        """Returns the number of Networks inside the collection.

        Returns:
            int: The number of Networks contained
        """
        return self.com_obj.Count

    def get_all_devices(self) -> dict:
        devices = dict()
        for index in range(1, self.count + 1):
            device_com_obj = self.com_obj.Item(index)
            device = Device(device_com_obj)
            devices[device.name] = device
        return devices


class Device:
    """The Device class represents one single device of CANalyzer.
    """
    def __init__(self, device_com_obj):
        self.com_obj = device_com_obj

    @property
    def name(self) -> str:
        """The name of the device.

        Returns:
            str: The name of the device.
        """
        return self.com_obj.Name
