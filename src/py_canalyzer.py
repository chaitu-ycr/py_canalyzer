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

    def __init__(self, py_log_dir='', user_capl_functions=tuple()) -> None:
        self.user_capl_function_names = user_capl_functions
        self.log = PyLogger(py_log_dir).log
        self.application = Application

    def get_application_info(self) -> str:
        """Vector CANalyzer Application Version.

        Returns:
            str: return Vector CANalyzer Application Version. "major.minor.build" -> "12.01.04"
        """
        cav = self.application.version
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
        self.application = Application(self.user_capl_function_names)
        if not auto_save:
            self.application.configuration.Modified = False
            self.log.info(f'CANalyzer cfg "Modified" parameter set to False to avoid error.')
        if os.path.isfile(canalyzer_cfg):
            self.log.info(f'CANalyzer cfg "{canalyzer_cfg}" found.')
            self.application.visible = visible
            self.application.open(canalyzer_cfg, auto_save, prompt_user)
            self.log.info(f'loaded CANalyzer config "{canalyzer_cfg}"')
            self.get_application_info()
        else:
            self.log.info(f'CANalyzer cfg "{canalyzer_cfg}" not found.')
            raise FileNotFoundError(f'CANalyzer cfg file "{canalyzer_cfg}" not found!')

    def new(self, auto_save=False, prompt_user=False) -> None:
        """Creates a new configuration.

        Args:
            auto_save (bool, optional): A boolean value that indicates whether the active configuration should be saved if it has been changed. Defaults to False.
            prompt_user (bool, optional): A boolean value that indicates whether the user should intervene in error situations. Defaults to False.
        """
        self.application.new(auto_save, prompt_user)

    def quit(self):
        """Quits the application.
        """
        self.application.quit()
        self.log.info('CANalyzer Application Closed.')

    def start_measurement(self, timeout=60) -> bool:
        r"""Starts the measurement.

        Args:
            timeout (int, optional): measurement start/stop event timeout in seconds. Defaults to 60.

        Returns:
            True if measurement started. else False.
        """
        self.application.measurement.meas_start_stop_timeout = timeout
        return self.application.measurement.start()

    def stop_measurement(self, timeout=60) -> bool:
        r"""Stops the measurement.

        Args:
            timeout (int, optional): measurement start/stop event timeout in seconds. Defaults to 60.

        Returns:
            True if measurement stopped. else False.
        """
        self.application.measurement.meas_start_stop_timeout = timeout
        return self.application.measurement.stop()

    def stop_ex_measurement(self, timeout=60) -> bool:
        r"""StopEx repairs differences in the behavior of the Stop method on deferred stops concerning simulated and real mode in CANalyzer.

        Args:
            timeout (int, optional): measurement start/stop event timeout in seconds. Defaults to 60.

        Returns:
            True if measurement stopped. else False.
        """
        self.application.measurement.meas_start_stop_timeout = timeout
        return self.application.measurement.stop_ex()

    def reset_measurement(self) -> bool:
        r"""reset the measurement.

        Returns:
            Measurement running status(True/False).
        """
        if self.application.measurement.running:
            self.application.measurement.stop()
        self.application.measurement.start()
        self.log.info(f'Resetted measurement.')
        return self.application.measurement.running

    def get_measurement_running_status(self) -> bool:
        r"""Returns the running state of the measurement.

        Returns:
            True if The measurement is running.
            False if The measurement is not running.
        """
        self.log.info(f'CANalyzer Measurement Running Status = {self.application.measurement.running}')
        return self.application.measurement.running

    def add_offline_source_log_file(self, absolute_log_file_path: str) -> bool:
        r"""this method adds offline source log file.

        Args:
            absolute_log_file_path (str): absolute path of offline source log file.

        Returns:
            bool: returns True if log file added or already available. False if log file not available.
        """
        if os.path.isfile(absolute_log_file_path):
            offline_sources = self.application.configuration.com_obj.OfflineSetup.Source.Sources
            file_already_added = any([file == absolute_log_file_path for file in offline_sources])
            if file_already_added:
                self.log.info(f'offline logging file ({absolute_log_file_path}) already added.')
            else:
                offline_sources.Add(absolute_log_file_path)
                self.log.info(f'added offline logging file ({absolute_log_file_path})')
            return True
        else:
            self.log.info(f'invalid logging file ({absolute_log_file_path}). Failed to add.')
            return False

    def start_measurement_in_animation_mode(self, animation_delay=100) -> None:
        r"""Starts the measurement in Animation mode.

        Args:
            animation_delay (int): The animation delay during the measurement in Offline Mode.
        """
        self.application.measurement.animation_delay = animation_delay
        self.application.measurement.animate()

    def break_measurement_in_offline_mode(self) -> None:
        r"""Interrupts the playback in Offline mode.
        """
        self.application.measurement.break_offline_mode()

    def reset_measurement_in_offline_mode(self) -> None:
        r"""Resets the measurement in Offline mode.
        """
        self.application.measurement.reset_offline_mode()

    def step_measurement_event_in_single_step(self) -> None:
        r"""Processes a measurement event in single step.
        """
        self.application.measurement.step()

    def get_measurement_index(self) -> int:
        r"""gets the measurement index for the next measurement.

        Returns:
            Measurement Index.
        """
        self.log.info(f'measurement_index value = {self.application.measurement.measurement_index}')
        return self.application.measurement.measurement_index

    def set_measurement_index(self, index: int) -> int:
        r"""sets the measurement index for the next measurement.

        Args:
            index (int): index value to set.

        Returns:
            Measurement Index value.
        """
        self.application.measurement.measurement_index = index
        return self.application.measurement.measurement_index

    def save_configuration(self) -> bool:
        r"""Saves the configuration.

        Returns:
            True if configuration saved. else False.
        """
        return self.application.configuration.save()

    def save_configuration_as(self, path: str, major: int, minor: int, create_dir=True) -> bool:
        r"""Saves the configuration as a different CANalyzer version.

        Args:
            path (str): The complete file name.
            major (int): The major version number of the target version.
            minor (int): The minor version number of the target version.
            create_dir (bool): create directory if not available. default value True.

        Returns:
            True if configuration saved. else False.
        """
        config_path = '\\'.join(path.split('\\')[:-1])
        if not os.path.exists(config_path) and create_dir:
            os.makedirs(config_path, exist_ok=True)
        if os.path.exists(config_path):
            self.application.configuration.save_as(path, major, minor, False)
            return self.application.configuration.saved
        else:
            self.log.info(f'tried creating {path}. but {config_path} directory not found.')
            return False

    def get_can_bus_statistics(self, channel: int) -> dict:
        r"""Returns CAN Bus Statistics.

        Args:
            channel (int): The channel of the statistic that is to be returned.

        Returns:
            CAN bus statistics.
        """
        conf_obj = self.application.configuration
        bus_types = {'CAN': 1, 'J1939': 2, 'TTP': 4, 'LIN': 5, 'MOST': 6, 'Kline': 14}
        bus_statistics_obj = conf_obj.com_obj.OnlineSetup.BusStatistics.BusStatistic(bus_types['CAN'], channel)
        statistics_info = {
            # The bus load
            'bus_load': bus_statistics_obj.BusLoad,
            # The controller status
            'chip_state': bus_statistics_obj.ChipState,
            # The number of Error Frames per second
            'error': bus_statistics_obj.Error,
            # The total number of Error Frames
            'error_total': bus_statistics_obj.ErrorTotal,
            # The number of messages with extended identifier per second
            'extended': bus_statistics_obj.Extended,
            # The total number of messages with extended identifier
            'extended_total': bus_statistics_obj.ExtendedTotal,
            # The number of remote messages with extended identifier per second
            'extended_remote': bus_statistics_obj.ExtendedRemote,
            # The total number of remote messages with extended identifier
            'extended_remote_total': bus_statistics_obj.ExtendedRemoteTotal,
            # The number of overload frames per second
            'overload': bus_statistics_obj.Overload,
            # The total number of overload frames
            'overload_total': bus_statistics_obj.OverloadTotal,
            # The maximum bus load in 0.01 %
            'peak_load': bus_statistics_obj.PeakLoad,
            # Returns the current number of the Rx error counter
            'rx_error_count': bus_statistics_obj.RxErrorCount,
            # The number of messages with standard identifier per second
            'standard': bus_statistics_obj.Standard,
            # The total number of remote messages with standard identifier
            'standard_total': bus_statistics_obj.StandardTotal,
            # The number of remote messages with standard identifier per second
            'standard_remote': bus_statistics_obj.StandardRemote,
            # The total number of remote messages with standard identifier
            'standard_remote_total': bus_statistics_obj.StandardRemoteTotal,
            # The current number of the Tx error counter
            'tx_error_count': bus_statistics_obj.TxErrorCount,
        }
        self.log.info(f'CAN Bus Statistics: {statistics_info}.')
        return statistics_info

    def get_canalyzer_version_info(self) -> dict:
        r"""The Version class represents the version of the CANalyzer application.

        Returns:
            "full_name" - The complete CANalyzer version.
            "name" - The CANalyzer version.
            "build" - The build number of the CANalyzer application.
            "major" - The major version number of the CANalyzer application.
            "minor" - The minor version number of the CANalyzer application.
            "patch" - The patch number of the CANalyzer application.
        """
        ver_obj = self.application.version
        version_info = {'full_name': ver_obj.full_name,
                        'name': ver_obj.name,
                        'build': ver_obj.build,
                        'major': ver_obj.major,
                        'minor': ver_obj.minor,
                        'patch': ver_obj.patch}
        self.log.info('> CANalyzer Application.Version <'.center(100, '='))
        for k, v in version_info.items():
            self.log.info(f'{k:<10}: {v}')
        self.log.info(''.center(100, '='))
        return version_info

    def get_bus_databases_info(self, bus: str) -> dict:
        """returns bus database info(path, channel, full_name).

        Args:
            bus (str): bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.

        Returns:
            bus database info {'path': 'value', 'channel': 'value', 'full_name': 'value'}
        """
        dbcs_info = dict()
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        db_objects = bus_obj.database_objects()
        for db_object in db_objects.values():
            dbcs_info[db_object.Name] = {'path': db_object.Path, 'channel': db_object.Channel, 'full_name': db_object.FullName}
        self.log.info(f'{bus} bus databases info -> {dbcs_info}.')
        return dbcs_info

    def get_signal_value(self, bus: str, channel: int, message: str, signal: str, raw_value=False) -> Union[float, int]:
        r"""get_signal_value Returns a Signal value.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.
            raw_value (bool): return raw value of the signal if true. Default(False) is physical value.

        Returns:
            signal value.
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_signal(channel, message, signal)
        signal_value = bus_obj.signal_get_raw_value(sig_obj) if raw_value else bus_obj.signal_get_value(sig_obj)
        self.log.info(f'value of signal({bus}{channel}.{message}.{signal})={signal_value}.')
        return signal_value

    def set_signal_value(self, bus: str, channel: int, message: str, signal: str, value: int, raw_value=False) -> None:
        r"""set_signal_value sets a value to Signal. Works only when messages are sent using CANalyzer IL.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.
            value (Union[float, int]): signal value.
            raw_value (bool): return raw value of the signal if true. Default(False) is physical value.
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_signal(channel, message, signal)
        if raw_value:
            bus_obj.signal_set_raw_value(sig_obj, value)
        else:
            bus_obj.signal_set_value(sig_obj, value)
        self.log.info(f'signal({bus}{channel}.{message}.{signal}) value set to {value}.')

    def get_signal_full_name(self, bus: str, channel: int, message: str, signal: str) -> str:
        """Determines the fully qualified name of a signal.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.

        Returns:
            str: The fully qualified name of a signal. The following format will be used for signals: <DatabaseName>::<MessageName>::<SignalName>
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_signal(channel, message, signal)
        signal_fullname = bus_obj.signal_full_name(sig_obj)
        self.log.info(f'signal({bus}{channel}.{message}.{signal}) full name = {signal_fullname}.')
        return signal_fullname

    def check_signal_online(self, bus: str, channel: int, message: str, signal: str) -> bool:
        r"""Checks whether the measurement is running and the signal has been received.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.

        Returns:
            TRUE if the measurement is running and the signal has been received. FALSE if not.
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_signal(channel, message, signal)
        sig_online_status = bus_obj.signal_is_online(sig_obj)
        self.log.info(f'signal({bus}{channel}.{message}.{signal}) online status = {sig_online_status}.')
        return sig_online_status

    def check_signal_state(self, bus: str, channel: int, message: str, signal: str) -> int:
        r"""Checks whether the measurement is running and the signal has been received.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.

        Returns:
            State of the signal.
                0- The default value of the signal is returned.
                1- The measurement is not running; the value set by the application is returned.
                2- The measurement is not running; the value of the last measurement is returned.
                3- The signal has been received in the current measurement; the current value is returned.
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_signal(channel, message, signal)
        sig_state = bus_obj.signal_state(sig_obj)
        self.log.info(f'signal({bus}{channel}.{message}.{signal}) state = {sig_state}.')
        return sig_state

    def get_j1939_signal_value(self, bus: str, channel: int, message: str, signal: str, source_addr: int, dest_addr: int, raw_value=False) -> Union[float, int]:
        r"""get_j1939_signal Returns a Signal object.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.
            source_addr (int): The source address of the ECU that sends the message.
            dest_addr (int): The destination address of the ECU that receives the message.
            raw_value (bool): return raw value of the signal if true. Default(False) is physical value.

        Returns:
            signal value.
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_j1939_signal(channel, message, signal, source_addr, dest_addr)
        signal_value = bus_obj.signal_get_raw_value(sig_obj) if raw_value else bus_obj.signal_get_value(sig_obj)
        self.log.info(f'value of signal({bus}{channel}.{message}.{signal})={signal_value}.')
        return signal_value

    def set_j1939_signal_value(self, bus: str, channel: int, message: str, signal: str, source_addr: int, dest_addr: int, value: Union[float, int], raw_value=False) -> None:
        r"""get_j1939_signal Returns a Signal object.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.
            source_addr (int): The source address of the ECU that sends the message.
            dest_addr (int): The destination address of the ECU that receives the message.
            value (Union[float, int]): signal value.
            raw_value (bool): return raw value of the signal if true. Default(False) is physical value.

        Returns:
            signal value.
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_j1939_signal(channel, message, signal, source_addr, dest_addr)
        if raw_value:
            bus_obj.signal_set_raw_value(sig_obj, value)
        else:
            bus_obj.signal_set_value(sig_obj, value)
        self.log.info(f'signal value set to {value}.')
        self.log.info(f'signal({bus}{channel}.{message}.{signal}) value set to {value}.')

    def get_j1939_signal_full_name(self, bus: str, channel: int, message: str, signal: str, source_addr: int, dest_addr: int) -> str:
        """Determines the fully qualified name of a signal.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.
            source_addr (int): The source address of the ECU that sends the message.
            dest_addr (int): The destination address of the ECU that receives the message.

        Returns:
            str: The fully qualified name of a signal. The following format will be used for signals: <DatabaseName>::<MessageName>::<SignalName>
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_j1939_signal(channel, message, signal, source_addr, dest_addr)
        signal_fullname = bus_obj.signal_full_name(sig_obj)
        self.log.info(f'signal({bus}{channel}.{message}.{signal}) full name = {signal_fullname}.')
        return signal_fullname

    def check_j1939_signal_online(self, bus: str, channel: int, message: str, signal: str, source_addr: int, dest_addr: int) -> bool:
        """Checks whether the measurement is running and the signal has been received.

        Args:
            bus (str): The Bus(CAN, LIN, FlexRay, MOST, AFDX, Ethernet) on which the signal is sent.
            channel (int): The channel on which the signal is sent.
            message (str): The name of the message to which the signal belongs.
            signal (str): The name of the signal.
            source_addr (int): The source address of the ECU that sends the message.
            dest_addr (int): The destination address of the ECU that receives the message.

        Returns:
            bool: TRUE: if the measurement is running and the signal has been received. FALSE: if not.
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_j1939_signal(channel, message, signal, source_addr, dest_addr)
        signal_online_status = bus_obj.signal_is_online(sig_obj)
        self.log.info(f'signal({bus}{channel}.{message}.{signal}) online status = {signal_online_status}.')
        return signal_online_status

    def check_j1939_signal_state(self, bus: str, channel: int, message: str, signal: str, source_addr: int, dest_addr: int) -> int:
        """Returns the state of the signal.

        Returns:
            int: State of the signal.
                possible values are:
                    0: The default value of the signal is returned.
                    1: The measurement is not running; the value set by the application is returned.
                    3: The signal has been received in the current measurement; the current value is returned.
        """
        bus_obj = self.application.bus
        if bus_obj.bus_type != bus:
            bus_obj.reinit_bus(bus_type=bus)
        sig_obj = bus_obj.get_j1939_signal(channel, message, signal, source_addr, dest_addr)
        signal_state = bus_obj.signal_state(sig_obj)
        self.log.info(f'signal({bus}{channel}.{message}.{signal}) state = {signal_state}.')
        return signal_state

    def ui_activate_desktop(self, name: str) -> None:
        r"""Activates the desktop with the given name.

        Args:
            name (str): The name of the desktop to be activated.
        """
        self.application.ui.activate_desktop(name)

    def ui_open_baudrate_dialog(self) -> None:
        r"""opens the dialog for configuring the bus parameters. Make sure Measurement stopped when using this method.
        """
        self.application.ui.open_baudrate_dialog()

    def write_text_in_write_window(self, text: str) -> None:
        r"""Outputs a line of text in the Write Window.
        Args:
            text (str): The text.
        """
        self.application.ui.write.output(text)

    def read_text_from_write_window(self) -> str:
        r"""read the text contents from Write Window.

        Returns:
            The text content.
        """
        return self.application.ui.write.text

    def clear_write_window_content(self) -> None:
        r"""Clears the contents of the Write Window.
        """
        self.application.ui.write.clear()

    def copy_write_window_content(self) -> None:
        r"""Copies the contents of the Write Window to the clipboard.
        """
        self.application.ui.write.copy()

    def enable_write_window_output_file(self, output_file: str, tab_index=None) -> None:
        r"""Enables logging of all outputs of the Write Window in the output file.

        Args:
            output_file (str): The complete path of the output file.
            tab_index (int, optional): The index of the page, for which logging of the output is to be activated. Defaults to None.
        """
        self.application.ui.write.enable_output_file(output_file, tab_index)

    def disable_write_window_output_file(self, tab_index=None) -> None:
        r"""Disables logging of all outputs of the Write Window.

        Args:
            tab_index (int, optional): The index of the page, for which logging of the output is to be activated. Defaults to None.
        """
        self.application.ui.write.disable_output_file(tab_index)

    def define_system_variable(self, sys_var_name: str, value: Union[int, float, str]) -> object:
        r"""define_system_variable Create a system variable with an initial value
        Args:
            sys_var_name (str): The name of the system variable. Ex- "sys_var_demo::speed"
            value (Union[int, float, str]): variable value. Default value 0.

        Returns:
            object: The new Variable object.
        """
        namespace_name = '::'.join(sys_var_name.split('::')[:-1])
        variable_name = sys_var_name.split('::')[-1]
        new_var_com_obj = None
        try:
            self.application.system.namespaces.add(namespace_name)
            namespaces = self.application.system.namespaces.fetch_namespaces()
            namespace = namespaces[namespace_name]
            new_var_com_obj = namespace.variables.add(variable_name, value)
            self.log.info(f'system variable({sys_var_name}) created and value set to {value}.')
        except Exception as e:
            self.log.info(f'failed to create system variable({sys_var_name}). {e}')
        return new_var_com_obj

    def get_system_variable_value(self, sys_var_name: str) -> Union[int, float, str, tuple, None]:
        r"""get_system_variable_value Returns a system variable value.

        Args:
            sys_var_name (str): The name of the system variable. Ex- "sys_var_demo::speed"

        Returns:
            System Variable value.
        """
        namespace = '::'.join(sys_var_name.split('::')[:-1])
        variable_name = sys_var_name.split('::')[-1]
        return_value = None
        try:
            namespace_com_object = self.application.system.com_obj.Namespaces(namespace)
            variable_com_object = namespace_com_object.Variables(variable_name)
            return_value = variable_com_object.Value
            self.log.info(f'system variable({sys_var_name}) value <- {return_value}.')
        except Exception as e:
            self.log.info(f'failed to get system variable({sys_var_name}) value. {e}')
        return return_value

    def set_system_variable_value(self, sys_var_name: str, value: Union[int, float, str]) -> None:
        r"""set_system_variable_value sets a value to system variable.

        Args:
            sys_var_name (str): The name of the system variable. Ex- "sys_var_demo::speed".
            value (Union[int, float, str]): variable value. supported CAPL system variable data types integer, double, string and data.
        """
        namespace = '::'.join(sys_var_name.split('::')[:-1])
        variable_name = sys_var_name.split('::')[-1]
        try:
            namespace_com_object = self.application.system.com_obj.Namespaces(namespace)
            variable_com_object = namespace_com_object.Variables(variable_name)
            if isinstance(variable_com_object.Value, int):
                variable_com_object.Value = int(value)
            elif isinstance(variable_com_object.Value, float):
                variable_com_object.Value = float(value)
            else:
                variable_com_object.Value = value
            self.log.info(f'system variable({sys_var_name}) value set to -> {value}.')
        except Exception as e:
            self.log.info(f'failed to set system variable({sys_var_name}) value. {e}')

    def set_system_variable_array_values(self, sys_var_name: str, value: tuple, index=0) -> None:
        r"""set_system_variable_array_values sets array of values to system variable.

        Args:
            sys_var_name (str): The name of the system variable. Ex- "sys_var_demo::speed"
            value (tuple): variable values. supported integer array or double array. please always give only one type.
            index (int): value of index where values will start updating. Defaults to 0.
        """
        namespace = '::'.join(sys_var_name.split('::')[:-1])
        variable_name = sys_var_name.split('::')[-1]
        try:
            namespace_com_object = self.application.system.com_obj.Namespaces(namespace)
            variable_com_object = namespace_com_object.Variables(variable_name)
            existing_variable_value = list(variable_com_object.Value)
            if (index + len(value)) <= len(existing_variable_value):
                final_value = existing_variable_value
                if isinstance(existing_variable_value[0], float):
                    final_value[index: index + len(value)] = (float(v) for v in value)
                else:
                    final_value[index: index + len(value)] = value
                variable_com_object.Value = tuple(final_value)
                wait(0.1)
                self.log.info(f'system variable({sys_var_name}) value set to -> {variable_com_object.Value}.')
            else:
                self.log.info(
                    f'failed to set system variable({sys_var_name}) value. check variable length and index value.')
        except Exception as e:
            self.log.info(f'failed to set system variable({sys_var_name}) value. {e}')

    def compile_all_capl_nodes(self) -> dict:
        r"""compiles all CAPL, XML and .NET nodes.
        """
        capl_obj = self.application.capl
        capl_obj.compile()
        wait(1)
        compile_result = capl_obj.compile_result()
        self.log.info(f'compiled all CAPL nodes successfully. result={compile_result["result"]}')
        return compile_result

    def call_capl_function(self, name: str, *arguments) -> bool:
        r"""Calls a CAPL function.
        Please note that the number of parameters must agree with that of the CAPL function.
        not possible to read return value of CAPL function at the moment. only execution status is returned.

        Args:
            name (str): The name of the CAPL function. Please make sure this name is already passed as argument during CANalyzer instance creation. see example for more info.
            arguments (tuple): Function parameters p1…p10 (optional).

        Returns:
            bool: CAPL function execution status. True-success, False-failed.
        """
        capl_obj = self.application.capl
        exec_sts = capl_obj.call_capl_function(self.application.measurement.user_capl_function_obj_dict[name], *arguments)
        self.log.info(f'triggered capl function({name}). execution status = {exec_sts}.')
        return exec_sts
