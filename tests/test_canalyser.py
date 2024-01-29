import os
import logging
from time import sleep as wait
from py_canalyzer import CANalyzer

file_path = os.path.dirname(os.path.abspath(__file__)).replace('/', '\\')
root_path = file_path
canalyzer_inst = CANalyzer(py_log_dir=fr'{root_path}\.py_canalyzer_log')
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


def test_bus_stats_canoe_ver_methods():
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
    canalyzer_inst.get_canalyzer_version_info()
    assert canalyzer_inst.start_measurement()
    wait(2)
    canalyzer_inst.get_can_bus_statistics(channel=1)
    assert canalyzer_inst.stop_measurement()
