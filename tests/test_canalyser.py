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
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=True, prompt_user=True)
    canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=False, auto_save=True, prompt_user=True)
    wait(5)
