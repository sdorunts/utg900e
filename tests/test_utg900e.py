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
    awg = UTG900E(addr)
    mock_rm.open_resource.assert_called_with(addr)
    assert awg.inst is mock_inst

def test_set_output(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst

    value_error_tests   = ((-1, False), (3, False))
    type_error_tests    = ((1, 0), (1, 1), (1, "True"))
    assert_calls_tests  = ((1, True), (1, False), (2, True), (2, False))

    for value_error_test in value_error_tests:
        channel, state = value_error_test
        with pytest.raises(ValueError):
            dev.set_output(channel, state)

    for type_error_test in type_error_tests:
        channel, state = type_error_test
        with pytest.raises(TypeError):
            dev.set_output(channel, state)

    for assert_calls_test in assert_calls_tests:
        channel, state = assert_calls_test
        dev.set_output(channel, state)
        mock_inst.write.assert_called_with(f":CHANnel{channel}:OUTPut {'ON' if state else 'OFF'}")


def test_get_output(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev = UTG900E()
    dev.inst = mock_inst
    dev.set_frequency(1, 1234.5)
    mock_inst.write.assert_called_with(":CHANnel1:BASE:FREQuency 1234.5")

def test_set_waveform(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.set_wave(2, "SINE")
    mock_inst.write.assert_called_with(":CHANnel2:BASE:WAVe SINE")

    value_error_tests   = (-1, 3, 0)
    assert_calls_tests  = (1, 2)

    for value_error_test in value_error_tests:
        channel = value_error_test
        with pytest.raises(ValueError):
            dev.get_output(channel)

    for assert_calls_test in assert_calls_tests:
        channel = assert_calls_test
        dev.get_output(channel)
        mock_inst.query.assert_called_with(f":CHANnel{channel}:OUTPut?")


def test_set_inversion(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.set_inversion(1)
    mock_inst.write.assert_called_with(":CHANnel1:INVersion OFF")


def test_get_inversion(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.get_inversion(1)
    mock_inst.query.assert_called_with(":CHANnel1:INVersion?")


def test_set_sync(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.set_sync(1, True)
    mock_inst.write.assert_called_with(":CHANnel1:OUTPut:SYNC ON")

def test_get_sync(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.get_sync(1)
    mock_inst.query.assert_called_with(":CHANnel1:OUTPut:SYNC?")

def test_limit_enable(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.limit_enable(1)
    mock_inst.write.assert_called_with(":CHANnel1:LIMit:ENABle ON")

def test_is_limit_enable(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.is_limit_enable(1)
    mock_inst.query.assert_called_with(":CHANnel1:LIMit:ENABle?")

def test_set_lower_limit(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.set_lower_limit(1, -0.01)
    mock_inst.write.assert_called_with(":CHANnel1:LIMit:LOWer -0.01")

def test_get_lower_limit(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.get_lower_limit(1)
    mock_inst.query.assert_called_with(":CHANnel1:LIMit:LOWer?")

def test_set_upper_limit(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.set_upper_limit(1, +0.12)
    mock_inst.write.assert_called_with(":CHANnel1:LIMit:UPPer 0.12")

def test_get_upper_limit(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.get_upper_limit(1)
    mock_inst.query.assert_called_with(":CHANnel1:LIMit:UPPer?")

def test_set_amplitude_unit(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    tests = ((1, "VRMS"), (1, "VPP"), (2, "VRMS"), (2, "VPP"))
    for test in tests:
        channel, unit = test
        dev.set_amplitude_unit(channel, unit)
        mock_inst.write.assert_called_with(f":CHANnel{channel}:AMPLitude:UNIT {unit}")

def test_get_amplitude_unit(mock_instrument):
    _, mock_inst = mock_instrument
    dev = UTG900E()
    dev.inst = mock_inst
    dev.get_amplitude_unit(1)
    mock_inst.query.assert_called_with(":CHANnel1:AMPLitude:UNIT?")

# def test_set_frequency(mock_instrument):
#     _, mock_inst = mock_instrument
#     dev = UTG900E()
#     dev.inst = mock_inst
#     dev.set_frequency(1, 1234.5)
#     mock_inst.write.assert_called_with(":CHANnel1:BASE:FREQuency 1234.5")
#
# def test_set_wave(mock_instrument):
#     _, mock_inst = mock_instrument
#     dev = UTG900E()
#     dev.inst = mock_inst
#     dev.set_wave(2, "SINE")
#     mock_inst.write.assert_called_with(":CHANnel2:BASE:WAVe SINE")
#
# def test_set_duty_validation(mock_instrument):
#     _, mock_inst = mock_instrument
#     dev = UTG900E()
#     dev.inst = mock_inst
#     with pytest.raises(ValueError):
#         dev.set_duty(1, 150)  # Grater than 100%

# def test_configure_square_calls_correct_setters(mock_instrument):
#     _, mock_inst = mock_instrument
#     dev = UTG900E()
#     dev.inst = mock_inst
#
#     dev.configure_square(channel=1, freq=500, amplitude=1.5, offset=0.2, phase=30, duty=60)
#
#     expected_calls = [
#         (":CHANnel1:MODe CONTINUE",),
#         (":CHANnel1:BASE:WAVe SQUARE",),
#         (":CHANnel1:BASE:FREQuency 500",),
#         (":CHANnel1:BASE:AMPLitude 1.5",),
#         (":CHANnel1:BASE:OFFSet 0.2",),
#         (":CHANnel1:BASE:PHAse 30",),
#         (":CHANnel1:BASE:DUTY 60",),
#     ]
#
#     actual_calls = [call.args for call in mock_inst.write.call_args_list]
#     assert actual_calls == expected_calls
#
# def test_configure_pulse_with_rise_fall(mock_instrument):
#     _, mock_inst = mock_instrument
#     dev = UTG900E()
#     dev.inst = mock_inst
#
#     dev.configure_pulse(channel=2, freq=1e3, amplitude=2, offset=0, phase=0,
#                         duty=50, rise_time=1e-6, fall_time=2e-6)
#
#     expected_fragments = [
#         "MODe CONTINUE",
#         "WAVe PULSE",
#         "FREQuency 1000.0",
#         "AMPLitude 2",
#         "OFFSet 0",
#         "PHAse 0",
#         "DUTY 50",
#         "PULSe:RISe 1e-06",
#         "PULSe:FALL 2e-06"
#     ]
#
#     commands = [call.args[0] for call in mock_inst.write.call_args_list]
#     for fragment in expected_fragments:
#         assert any(fragment in cmd for cmd in commands)
