# About [py_canalyzer](https://github.com/chaitu-ycr/py_canalyzer)

Python 🐍 Package for controlling Vector CANalyzer 🛶 Tool

fork [this repo](https://github.com/chaitu-ycr/py_canalyzer/fork) and create pull request to contribute back to this project.

for ideas/discussions please create new discussion [here](https://github.com/chaitu-ycr/py_canalyzer/discussions)

create issue or request feature [here](https://github.com/chaitu-ycr/py_canalyzer/issues/new/choose)

## GitHub Releases 👉 [link](https://github.com/chaitu-ycr/py_canalyzer/releases)

## PyPi Package 👉 [link](https://pypi.org/project/py_canalyzer/)

## Prerequisites [link](https://chaitu-ycr.github.io/py_canalyzer/002_prerequisites/)

## Python environment setup instructions [link](https://chaitu-ycr.github.io/py_canalyzer/003_environment_setup/)

## Install [py_canalyzer](https://pypi.org/project/py_canalyzer/) package

```bat
pip install py_canalyzer --upgrade
```

## Documentation Links

### example use cases 👉 [link](https://chaitu-ycr.github.io/py_canalyzer/004_usage/)

### package reference doc 👉 [link](https://chaitu-ycr.github.io/py_canalyzer/999_reference/)

## Sample Example

```python
# Import CANalyzer module
from py_canalyzer import CANalyzer

# create CANalyzer object
canalyzer_inst = CANalyzer()

# open CANalyzer configuration. Replace CANalyzer_cfg with yours.
canalyzer_inst.open(canalyzer_cfg=r'tests\demo_cfg\demo.cfg')

# print installed CANalyzer application version
canalyzer_inst.get_canalyzer_version_info()

# Start CANalyzer measurement
canalyzer_inst.start_measurement()

# get signal value. Replace arguments with your message and signal data.
sig_val = canalyzer_inst.get_signal_value('CAN', 1, 'LightState', 'FlashLight')
print(sig_val)

# Stop CANalyzer Measurement
canalyzer_inst.stop_measurement()

# Quit / Close CANalyzer configuration
canalyzer_inst.quit()
```
