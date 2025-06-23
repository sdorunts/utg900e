import pytest
from unittest.mock import MagicMock, patch
from utg900e import UTG900E

@pytest.fixture
def mock_instrument():
    with patch("pyvisa.ResourceManager") as mock_rm_class:
        mock_rm = MagicMock()
        mock_inst = MagicMock()
        mock_rm.open_resource.return_value = mock_inst
        mock_rm_class.return_value = mock_rm
        yield mock_rm, mock_inst

def test_connection(mock_instrument):
    mock_rm, mock_inst = mock_instrument
    addr = "USB0::0x5345::0x1234::SN20220718::INSTR"
    device = UTG900E(addr)
    mock_rm.open_resource.assert_called_with(addr)
    assert device.inst is mock_inst

def test_set_frequency(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.set_frequency(1, 1234.5)
    mock_inst.write.assert_called_with(":CHANnel1:BASE:FREQuency 1234.5")

def test_set_waveform(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.set_waveform(2, "SINE")
    mock_inst.write.assert_called_with(":CHANnel2:BASE:WAVe SINE")

def test_set_duty_validation(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    with pytest.raises(ValueError):
        dev.set_duty(1, 150)  # Grater than 100%

def test_configure_square_calls_correct_setters(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst

    dev.configure_square(channel=1, freq=500, amplitude=1.5, offset=0.2, phase=30, duty=60)

    expected_calls = [
        (":CHANnel1:MODe CONTINUE",),
        (":CHANnel1:BASE:WAVe SQUARE",),
        (":CHANnel1:BASE:FREQuency 500",),
        (":CHANnel1:BASE:AMPLitude 1.5",),
        (":CHANnel1:BASE:OFFSet 0.2",),
        (":CHANnel1:BASE:PHAse 30",),
        (":CHANnel1:BASE:DUTY 60",),
    ]

    actual_calls = [call.args for call in mock_inst.write.call_args_list]
    assert actual_calls == expected_calls

def test_configure_pulse_with_rise_fall(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst

    dev.configure_pulse(channel=2, freq=1e3, amplitude=2, offset=0, phase=0,
                        duty=50, rise_time=1e-6, fall_time=2e-6)

    expected_fragments = [
        "MODe CONTINUE",
        "WAVe PULSE",
        "FREQuency 1000.0",
        "AMPLitude 2",
        "OFFSet 0",
        "PHAse 0",
        "DUTY 50",
        "PULSe:RISe 1e-06",
        "PULSe:FALL 2e-06"
    ]

    commands = [call.args[0] for call in mock_inst.write.call_args_list]
    for fragment in expected_fragments:
        assert any(fragment in cmd for cmd in commands)
