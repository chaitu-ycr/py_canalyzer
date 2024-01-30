# Usage

## Import CANalyzer module.

```python
# Import CANalyzer module. Always do this in your root script.
from py_canalyzer import CANalyzer

# create CANalyzer object. arguments are optional. Avoid creating multiple CANalyzer instances.
canalyzer_inst = CANalyzer(py_log_dir=fr'{root_path}\.py_canalyzer_log', user_capl_functions=('addition_function', 'hello_world'))
```

## Example use cases

### open CANalyzer, start measurement, get version info, stop measurement and close CANalyzer configuration

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.start_measurement()
canalyzer_version_info = canalyzer_inst.get_canalyzer_version_info()
canalyzer_inst.stop_measurement()
canalyzer_inst.quit()
```

### restart/reset running measurement

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.start_measurement()
canalyzer_inst.reset_measurement()
canalyzer_inst.stop_ex_measurement()
```

### get/set canalyzer measurement index

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
meas_index_value = canalyzer_inst.get_measurement_index()
canalyzer_inst.start_measurement()
canalyzer_inst.stop_measurement()
meas_index_value = canalyzer_inst.get_measurement_index()
canalyzer_inst.set_measurement_index(meas_index_value + 1)
meas_index_new = canalyzer_inst.get_measurement_index()
canalyzer_inst.reset_measurement()
canalyzer_inst.stop_measurement()
```

### save canalyzer config to a different version with different name

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.save_configuration_as(path=fr'D:\py_canalyzer\demo_cfg\CANMainDemo\CANMainDemo_v11.cfg', major=11, minor=0, create_dir=True)
```

### get CAN bus statistics of CAN channel 1

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.start_measurement()
wait(2)
canalyzer_inst.get_can_bus_statistics(channel=1)
canalyzer_inst.stop_measurement()
```

### get bus signal value, check signal state and get signal full name

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.start_measurement()
wait(1)
canalyzer_inst.get_signal_full_name(bus='CAN', channel=1, message='EngineData', signal='EngSpeed')
canalyzer_inst.get_signal_value(bus='CAN', channel=1, message='EngineData', signal='EngSpeed', raw_value=False)
wait(1)
canalyzer_inst.check_signal_online(bus='CAN', channel=1, message='EngineData', signal='EngSpeed')
canalyzer_inst.check_signal_state(bus='CAN', channel=1, message='EngineData', signal='EngSpeed')
canalyzer_inst.get_signal_value(bus='CAN', channel=1, message='EngineData', signal='EngSpeed', raw_value=True)
canalyzer_inst.stop_measurement()
```

### clear write window / read text from write window / control write window output file

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.enable_write_window_output_file(fr'{file_path}\demo_cfg\Logs\write_win.txt')
wait(1)
canalyzer_inst.start_measurement()
canalyzer_inst.clear_write_window_content()
wait(1)
canalyzer_inst.write_text_in_write_window("hello from py_canalyzer!")
wait(1)
text = canalyzer_inst.read_text_from_write_window()
canalyzer_inst.stop_measurement()
canalyzer_inst.disable_write_window_output_file()
wait(1)
```

### switch between canalyzer desktops

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.ui_activate_desktop('Analysis')
```

### get/set system variable or define system variable

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.start_measurement()
wait(1)
canalyzer_inst.set_system_variable_value('demo::level_two_1::sys_var2', 20)
canalyzer_inst.set_system_variable_value('demo::string_var', 'hey hello this is string variable')
canalyzer_inst.set_system_variable_value('demo::data_var', 'hey hello this is data variable')
canalyzer_inst.set_system_variable_array_values('demo::int_array_var', (00, 11, 22, 33, 44, 55, 66, 77, 88, 99))
wait(0.1)
sys_var_val = canalyzer_inst.get_system_variable_value('demo::level_two_1::sys_var2')
sys_var_val = canalyzer_inst.get_system_variable_value('demo::data_var')
canalyzer_inst.stop_measurement()
# define system variable and use it in measurement
canalyzer_inst.define_system_variable('sys_demo::demo', 1)
canalyzer_inst.save_configuration()
canalyzer_inst.start_measurement()
wait(1)
sys_var_val = canalyzer_inst.get_system_variable_value('sys_demo::demo')
canalyzer_inst.stop_measurement()
```

### compile CAPL nodes and call capl function

```python
canalyzer_inst.open(canalyzer_cfg=fr'{file_path}\demo_cfg\CANMainDemo\CANMainDemo.cfg', visible=True, auto_save=False, prompt_user=False)
canalyzer_inst.compile_all_capl_nodes()
canalyzer_inst.start_measurement()
wait(1)
canalyzer_inst.call_capl_function('addition_function', 100, 200)
canalyzer_inst.call_capl_function('hello_world')
canalyzer_inst.stop_measurement()
```
