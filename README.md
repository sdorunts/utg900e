# UTG900E Python Library

A Python library for controlling UTG900E series signal generators via SCPI commands using VISA interface.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![PyPI Version](https://img.shields.io/pypi/v/utg900e.svg)](https://pypi.org/project/utg900e/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Complete SCPI Command Support**: Full control over UTG900E series signal generators
- **Easy-to-Use Interface**: High-level Python methods for common operations
- **VISA Backend Support**: Compatible with NI-VISA, pyvisa-py, and other VISA implementations
- **Type Hints**: Better code completion and error detection
- **Comprehensive Error Handling**: Robust communication with instruments

## Installation

### From PyPI
```bash
pip install utg900e
```

### From Source
```bash
git clone https://github.com/yourusername/utg900e.git
cd utg900e
pip install .
```

## Requirements

- Python 3.7 or higher
- PyVISA >= 1.11.0
- A VISA backend (NI-VISA, pyvisa-py, etc.)
- colorlog >= 6.9.0 (for enhanced logging)

## Quick Start

```python
from utg900e import UTG900E

address = "USB0::0x6656::0x0834::AWG1524090001::INSTR"

gen = UTG900E(address)

# Basic configuration
gen.set_frequency(channel=1, freq_hz=1000)      # 1 kHz
gen.set_amplitude(channel=1, amplitude_v=1.0)   # 1 Vpp
gen.set_wave(channel=1, wave='SIN')             # Sine wave
gen.set_output(channel=1, state=True)           # Enable output

# Query instrument information
print(f"I: {gen.identify()}")
# print(f"Model: {gen.get_model()}")
# print(f"Serial Number: {gen.get_serial_number()}")

# Disconnect
gen.close()
```

## Connection Methods

### Ethernet Connection
```python
# # Direct IP connection
# gen = UTG900E("TCPIP0::192.168.1.100::inst0::INSTR")
# 
# # With hostname
# gen = UTG900E("TCPIP0::hostname::inst0::INSTR")
```

### USB Connection
```python
from utg900e import UTG900E

gen = UTG900E("USB0::0x6656::0x0834::AWG1524090001::INSTR")
```


## Basic Usage Examples

### Generating Different Waveforms

```python
from utg900e import UTG900E

gen = UTG900E("USB0::0x6656::0x0834::AWG1524090001::INSTR")

# Sine wave
gen.set_wave(channel=1, wave='SIN')
gen.set_frequency(channel=1, freq_hz=1000)      # 1 kHz
gen.set_amplitude(channel=1, amplitude_v=2.0)   # 2 Vpp
# OR
gen.configure_sine(channel=1, freq=1000, amp=2.0)

# Square wave
gen.set_wave(channel=1, wave='SQUARE')
gen.set_frequency(channel=1, freq_hz=5000)  # 5 kHz
gen.set_duty(channel=1, duty_percent=30)    # 30% duty cycle
# OR
gen.configure_square(channel=1, freq=5000, duty=30)
```

### Frequency and Amplitude Control

```python
from utg900e import UTG900E

gen = UTG900E("USB0::0x6656::0x0834::AWG1524090001::INSTR")

# Set frequency in different units
gen.set_frequency(1, 1000)        # 1 kHz
gen.set_frequency(1, 1.5e6)       # 1.5 MHz
gen.set_frequency(1, 0.5)         # 0.5 Hz

# Set amplitude in different units
gen.set_amplitude(1, 1.0)         # 1 Vpp
gen.set_amplitude(1, 0.5)         # 500 mVpp
gen.set_amplitude(1, 2.5)         # 2.5 Vpp

# Set DC offset
gen.set_offset(1, 0.1)            # 100 mV DC offset
```

### Output Control

```python
from utg900e import UTG900E

gen = UTG900E("USB0::0x6656::0x0834::AWG1524090001::INSTR")

gen_channel     = 1
enable_output   = True
disable_output  = False

# Enable/disable output
gen.set_output(gen_channel, enable_output)              # OR gen.output_on(gen_channel)
print(f"Output state: {gen.get_output(gen_channel)}")   # Should return True

gen.set_output(gen_channel)                             # OR gen.output_off(gen_channel)
print(f"Output state: {gen.get_output(gen_channel)}")   # Should return False

# Toggle output
if gen.get_output(gen_channel):
    gen.output_off(gen_channel)
else:
    gen.output_on(gen_channel)
```

### Debug Mode

Enable debug logging to see all SCPI commands and responses:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from utg900e import UTG900E
gen = UTG900E("TCPIP0::192.168.1.100::inst0::INSTR")
```

### VISA Backend Issues

```python
import pyvisa as visa

# Check available backends
rm = visa.ResourceManager()
print(f"VISA backend: {rm}")

# List all resources
resources = rm.list_resources()
print(f"Available resources: {resources}")

# If no resources found, try different backend
# rm = visa.ResourceManager('@py')  # Use pyvisa-py backend
```

## Supported Models

- UTG900E series signal gens
- Compatible with other SCPI-compliant instruments (partial support)

## Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup
```bash
git clone https://github.com/yourusername/utg900e-lib.git
cd utg900e-lib
pip install -e ".[dev]"
pytest  # Run tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any problems or have questions:

1. Check the [issues page](https://github.com/yourusername/utg900e-lib/issues)
2. Create a new issue with detailed description
3. Contact: sdorunts@yandex.com

## Changelog

### v0.1.0
- Initial release
- Basic waveform control
- Modulation functions
- Sweep functions
```
