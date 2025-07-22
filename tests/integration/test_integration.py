import pytest
import random
import time
from utg900e import UTG900E


@pytest.fixture
def device():
    address = "USB0::0x6656::0x0834::AWG1524090004::INSTR"
    dev = UTG900E(address)
    yield dev


def test_limit_enable(device):
    set_param = ((1, False), (1, True), (2, False), (2, True))
    for channel, lim_en in set_param:
        device.limit_enable(channel, lim_en)
        get_lim_en = device.is_limit_enable(channel)
        assert lim_en == get_lim_en


def test_set_load(device):
    number_of_tests = 10
    random.seed(120)  # The fixed seed for reproducibility. Any number works
    set_param = ([[1, 0.2, 1], [2, 10001, 10000], [1, 50, 50], [2, 10000, 10000]] +
                 [[random.randint(1, 2), val := random.randint(1, 9999), val] for __ in range(number_of_tests)])
    for channel, set_load, expected_load in set_param:
        device.set_load(channel, set_load)
        get_load = device.get_load(channel)
        assert get_load == expected_load


def test_set_lower_limit(device):
    number_of_tests = 30
    random.seed(160)  # The fixed seed for reproducibility. Any number works
    set_param = [
        [
            random.randint(1, 2),  # channel
            random.randint(1, 99),  # load
            round(random.uniform(-10, 10), 3),  # limit_v
        ]
        for __ in range(number_of_tests)
    ]
    for channel, set_load, set_limit in set_param:
        device.set_load(channel, set_load)
        upper_limit = round(10 * set_load / (50 + set_load), 3)
        lower_limit = -1 * upper_limit
        if lower_limit <= set_limit <= upper_limit:
            expected_limit = set_limit
        elif set_limit < lower_limit:
            expected_limit = lower_limit
        else:
            expected_limit = upper_limit
        device.set_lower_limit(channel, set_limit)
        get_limit_v = device.get_lower_limit(channel)
        # print(f"set_load: {set_load}\nset_limit: {set_limit}\nlower_limit: {lower_limit}\nupper_limit: {upper_limit}\nexpected_limit: {expected_limit}\nget_limit_v: {get_limit_v}\n")
        assert get_limit_v == expected_limit


def test_set_upper_limit(device):
    number_of_tests = 30
    random.seed(200)  # The fixed seed for reproducibility. Any number works
    set_param = [
        [
            random.randint(1, 2),  # channel
            random.randint(1, 99),  # load
            round(random.uniform(-10, 10), 3),  # limit_v
        ]
        for __ in range(number_of_tests)
    ]
    for channel, set_load, set_limit in set_param:
        device.set_load(channel, set_load)
        upper_limit = round(10 * set_load / (50 + set_load), 3)
        lower_limit = -1 * upper_limit
        if lower_limit <= set_limit <= upper_limit:
            expected_limit = set_limit
        elif set_limit < lower_limit:
            expected_limit = lower_limit
        else:
            expected_limit = upper_limit
        device.set_upper_limit(channel, set_limit)
        get_limit_v = device.get_upper_limit(channel)
        # print(f"set_load: {set_load}\nset_limit: {set_limit}\nlower_limit: {lower_limit}\nupper_limit: {upper_limit}\nexpected_limit: {expected_limit}\nget_limit_v: {get_limit_v}\n")
        assert get_limit_v == expected_limit


def test_set_wave(device):
    random.seed(100)
    set_param = [[random.randint(1, 2), wave] for wave in device.available_waves]
    for channel, set_wave in set_param:
        device.set_wave(channel, set_wave)
        get_wave = device.get_wave(channel)
        assert get_wave == set_wave


def test_set_frequency(device):
    number_of_tests = 10
    random.seed(100)  # The fixed seed for reproducibility. Any number works
    set_param = [[random.randint(1, 2), round(random.uniform(0, 100000), 2)] for __ in range(number_of_tests)]
    for channel, set_freq in set_param:
        device.set_frequency(channel, set_freq)
        get_freq = round(device.get_frequency(channel), 2)
        assert get_freq == set_freq


def test_set_period(device):
    number_of_tests = 20
    higher_value = 1e6
    lower_value = 1.7e-08
    random.seed(100)
    set_param = [[1, 0.9 * lower_value, lower_value], [1, 1.1 * higher_value, higher_value], [1, 0, lower_value]] + \
                [[
                    random.randint(1, 2),
                    set_val := random.randint(0, int(2e6)),
                    set_val if lower_value <= set_val <= higher_value else (
                        higher_value if set_val > higher_value else lower_value)
                ] for __ in range(number_of_tests)]
    for channel, set_period, expected_period in set_param:
        device.set_period(channel, set_period)
        get_period = device.get_period(channel)
        assert get_period == expected_period
    # print()
    # print(*set_param, sep='\n')


def test_set_phase(device):
    number_of_tests = 20
    higher_value = 360
    lower_value = -360
    random.seed(100)
    set_param = [[1, -500, -360], [1, 500, 360]] + \
                [[
                    random.randint(1, 2),
                    set_val := round(random.uniform(-500, 500), 2),
                    set_val if lower_value <= set_val <= higher_value else (
                        higher_value if set_val > higher_value else lower_value)
                ] for __ in range(number_of_tests)]
    for channel, set_phase, expected_phase in set_param:
        device.set_phase(channel, set_phase)
        get_phase = device.get_phase(channel)
        assert get_phase == expected_phase
    # print()
    # print(*set_param, sep='\n')


def test_set_amplitude(device):
    number_of_tests = 20
    random.seed(100)
    # device.limit_enable(1, False)
    device.set_amplitude(1, 6)
    pass


def test_set_offset(device):
    pass
