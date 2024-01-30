import os
import logging
from time import sleep as wait
from py_canalyzer import CANalyzer

file_path = os.path.dirname(os.path.abspath(__file__)).replace('/', '\\')
root_path = file_path
canalyzer_inst = CANalyzer(py_log_dir=fr'{root_path}\.py_canalyzer_log', user_capl_functions=('addition_function', 'hello_world'))
logger_inst = logging.getLogger('CANALYZER_LOG')

def test_open_new_quit_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    canalyzer_inst.new(auto_save=True, prompt_user=False)
    canalyzer_inst.new(auto_save=True, prompt_user=True)
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=False, auto_save=True, prompt_user=True)
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=True, prompt_user=True)
    canalyzer_inst.quit()
    wait(5)


def test_meas_start_stop_restart_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    assert canalyzer_inst.start_measurement()
    assert canalyzer_inst.stop_measurement()
    assert canalyzer_inst.start_measurement()
    assert canalyzer_inst.reset_measurement()
    assert canalyzer_inst.get_measurement_running_status()
    assert canalyzer_inst.stop_ex_measurement()
    assert not canalyzer_inst.get_measurement_running_status()


def test_meas_index_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    canalyzer_inst.get_measurement_index()
    assert canalyzer_inst.start_measurement()
    assert canalyzer_inst.stop_measurement()
    meas_index_old = canalyzer_inst.get_measurement_index()
    canalyzer_inst.set_measurement_index(meas_index_old + 1)
    meas_index_new = canalyzer_inst.get_measurement_index()
    assert meas_index_new == meas_index_old + 1
    canalyzer_inst.reset_measurement()
    assert canalyzer_inst.stop_measurement()


def test_meas_save_saveas_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    assert canalyzer_inst.save_configuration()
    canalyzer_inst.new(auto_save=True)
    assert canalyzer_inst.save_configuration_as(path=fr'{file_path}\demo_cfg\CANMainDemo\demo_v16.cfg', major=16, minor=0, create_dir=True)
    wait(1)


def test_bus_stats_canalyzer_ver_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    canalyzer_inst.get_canalyzer_version_info()
    assert canalyzer_inst.start_measurement()
    wait(2)
    canalyzer_inst.get_can_bus_statistics(channel=1)
    assert canalyzer_inst.stop_measurement()


def test_ui_class_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    canalyzer_inst.ui_activate_desktop('Analysis')
    canalyzer_inst.enable_write_window_output_file(fr'{file_path}\demo_cfg\CANMainDemo\Logs\write_win.txt')
    wait(1)
    assert canalyzer_inst.start_measurement()
    canalyzer_inst.clear_write_window_content()
    wait(1)
    canalyzer_inst.write_text_in_write_window("hello from py_canalyzer!")
    wait(1)
    text = canalyzer_inst.read_text_from_write_window()
    assert canalyzer_inst.stop_measurement()
    canalyzer_inst.disable_write_window_output_file()
    assert "hello from py_canalyzer!" in text
    wait(1)


def test_system_variable_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    assert canalyzer_inst.start_measurement()
    wait(1)
    canalyzer_inst.set_system_variable_value('demo::level_two_1::sys_var2', 20)
    sys_var_val = canalyzer_inst.get_system_variable_value('demo::level_two_1::sys_var2')
    canalyzer_inst.set_system_variable_array_values('demo::int_array_var', (00, 11, 22, 33, 44, 55, 66, 77, 88, 00))
    assert canalyzer_inst.get_system_variable_value('demo::int_array_var') == (00, 11, 22, 33, 44, 55, 66, 77, 88, 00)
    canalyzer_inst.set_system_variable_array_values('demo::double_array_var', (00.0, 11.1, 22.2, 33.3, 44.4))
    assert canalyzer_inst.get_system_variable_value('demo::double_array_var') == (00.0, 11.1, 22.2, 33.3, 44.4)
    canalyzer_inst.set_system_variable_value('demo::string_var', 'hey hello this is string variable')
    assert canalyzer_inst.get_system_variable_value('demo::string_var') == 'hey hello this is string variable'
    canalyzer_inst.set_system_variable_value('demo::data_var', (0x0A, 0x1B, 0x2C, 0x3D, 0x4E, 0x5F))
    assert canalyzer_inst.get_system_variable_value('demo::data_var') == (0x0A, 0x1B, 0x2C, 0x3D, 0x4E, 0x5F)
    assert canalyzer_inst.stop_measurement()
    assert sys_var_val == 20
    canalyzer_inst.define_system_variable('sys_demo::demo', 1)
    canalyzer_inst.save_configuration()
    assert canalyzer_inst.start_measurement()
    wait(1)
    sys_var_val = canalyzer_inst.get_system_variable_value('sys_demo::demo')
    assert sys_var_val == 1
    assert canalyzer_inst.stop_measurement()
    wait(1)


def test_capl_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    canalyzer_inst.compile_all_capl_nodes()
    assert canalyzer_inst.start_measurement()
    wait(1)
    assert canalyzer_inst.call_capl_function('addition_function', 100, 200)
    assert canalyzer_inst.call_capl_function('hello_world')
    assert canalyzer_inst.stop_measurement()


def test_bus_signal_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    assert canalyzer_inst.start_measurement()
    wait(1)
    canalyzer_inst.get_signal_full_name(bus='CAN', channel=1, message='EngineData', signal='EngSpeed')
    canalyzer_inst.get_signal_value(bus='CAN', channel=1, message='EngineData', signal='EngSpeed', raw_value=False)
    wait(1)
    assert canalyzer_inst.check_signal_online(bus='CAN', channel=1, message='EngineData', signal='EngSpeed')
    canalyzer_inst.check_signal_state(bus='CAN', channel=1, message='EngineData', signal='EngSpeed')
    canalyzer_inst.get_signal_value(bus='CAN', channel=1, message='EngineData', signal='EngSpeed', raw_value=True)
    assert canalyzer_inst.stop_measurement()
