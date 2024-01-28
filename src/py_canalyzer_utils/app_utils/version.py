# Import Python Libraries here
import logging
import win32com.client


class Version:
    """The Version object represents the version of the CANalyzer application.
    """

    def __init__(self, app_com_obj):
        self.__log = logging.getLogger('CANALYZER_LOG')
        self.com_obj = win32com.client.Dispatch(app_com_obj.Version)

    @property
    def build(self) -> int:
        """Returns the build number of the CANalyzer application.

        Returns:
            int: The build number of the CANalyzer application.
        """
        return self.com_obj.Build

    @property
    def full_name(self) -> str:
        """Determines the complete path of the object.

        Returns:
            str: The complete CANalyzer version in the following format: "Vector CANalyzer /run 6.0.50" or "Vector CANalyzer.LIN /run 6.0.50".
        """
        return self.com_obj.FullName

    @full_name.setter
    def full_name(self, full_name: str) -> None:
        """Sets the complete path of the object.

        Args:
            full_name (str): The complete CANalyzer version in the following format: "Vector CANalyzer /run 6.0.50" or "Vector CANalyzer.LIN /run 6.0.50".
        """
        self.com_obj.FullName = full_name
        self.__log.info(f'CANalyzer version set to {full_name}.')

    @property
    def major(self) -> int:
        """Returns the major version number of the CANalyzer application.

        Returns:
            int: The major version number of the CANalyzer application.
        """
        return self.com_obj.major

    @property
    def minor(self) -> int:
        """Returns the Minor version number of the CANalyzer application.

        Returns:
            int: The Minor version number of the CANalyzer application.
        """
        return self.com_obj.minor

    @property
    def name(self) -> str:
        """Returns the name of the object.

        Returns:
            str: The CANalyzer version in the following format: "CANalyzer 5.1 SP2" (with Service Pack) or "CANalyzer.LIN 5.1" (without Service Pack).
        """
        return self.com_obj.Name

    @property
    def patch(self) -> int:
        """Returns the patch number of the CANalyzer application.

        Returns:
            int: The patch number of the CANalyzer application.
        """
        return self.com_obj.Patch
