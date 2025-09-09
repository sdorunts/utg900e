import json
import logging
import tracemalloc
import pytest
import random
from utg900e import UTG900E
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN


tracemalloc.start(20)

_limit_calc = lambda x: 10 if x == 10000 else round(10 * x / (50 + x), 3)
_round_math = lambda number, digits=0: float(Decimal(str(number)).quantize(Decimal(f"1e-{digits}"), rounding=ROUND_HALF_UP))
_truncate_decimal = lambda number, digits=0: float(Decimal(str(number)).quantize(Decimal(f"1e-{digits}"), rounding=ROUND_DOWN))
_vpp_vrms_coeff_for_waves = {
    'SINe': {'vpp_to_vrms': 0.35355, 'vrms_to_vpp': 2.8284542497525105},
    'SQUare': {'vpp_to_vrms': 0.5, 'vrms_to_vpp': 2.0},
    'PULSe': {'vpp_to_vrms': 0.5, 'vrms_to_vpp': 2.0},
    'RAMP': {'vpp_to_vrms': 0.2887, 'vrms_to_vpp': 3.4638032559750607},
    'AbsSine': {'vpp_to_vrms': 0.5, 'vrms_to_vpp': 2.0},
    'AmpALT': {'vpp_to_vrms': 0.5, 'vrms_to_vpp': 2.0},
    'AttALT': {'vpp_to_vrms': 0.5, 'vrms_to_vpp': 2.0},
    'Cardiac': {'vpp_to_vrms': 0.5, 'vrms_to_vpp': 2.0},
    'CosH': {'vpp_to_vrms': 0.3323, 'vrms_to_vpp': 3.009328919650918},
    'EEG': {'vpp_to_vrms': 0.15025, 'vrms_to_vpp': 6.655574043261232},
    'EOG': {'vpp_to_vrms': 0.1407, 'vrms_to_vpp': 7.107320540156361},
    'GaussianMonopulse': {'vpp_to_vrms': 0.36920000000000003, 'vrms_to_vpp': 2.7085590465872156},
    'GaussPulse': {'vpp_to_vrms': 0.39275000000000004, 'vrms_to_vpp': 2.546148949713558},
    'LogNormal': {'vpp_to_vrms': 0.1765, 'vrms_to_vpp': 5.6657223796034},
    'Lorentz': {'vpp_to_vrms': 0.15489999999999998, 'vrms_to_vpp': 6.45577792123951},
    'Pulseilogram': {'vpp_to_vrms': 0.27080000000000004, 'vrms_to_vpp': 3.692762186115214},
    'Radar': {'vpp_to_vrms': 0.4473, 'vrms_to_vpp': 2.23563603845294},
    'Sinc': {'vpp_to_vrms': 0.3806, 'vrms_to_vpp': 2.627430373095113},
    'SineVer': {'vpp_to_vrms': 0.4667, 'vrms_to_vpp': 2.142704092564817},
    'StairUD': {'vpp_to_vrms': 0.31675, 'vrms_to_vpp': 3.1570639305445933},
    'StepResp': {'vpp_to_vrms': 0.45095, 'vrms_to_vpp': 2.2175407473112316},
    'Trapezia': {'vpp_to_vrms': 0.32475, 'vrms_to_vpp': 3.079291762894534},
    'TV': {'vpp_to_vrms': 0.25070000000000003, 'vrms_to_vpp': 3.9888312724371757},
    'VOICE': {'vpp_to_vrms': 0.3227, 'vrms_to_vpp': 3.098853424233034},
    'Log_up': {'vpp_to_vrms': 0.4157, 'vrms_to_vpp': 2.405580947798893},
    'Log_down': {'vpp_to_vrms': 0.37985, 'vrms_to_vpp': 2.6326181387389758},
    'Tri_up': {'vpp_to_vrms': 0.40225, 'vrms_to_vpp': 2.4860161591050343},
    'Tri_down': {'vpp_to_vrms': 0.16885, 'vrms_to_vpp': 5.922416345869115},
    'NOISe': {'vpp_to_vrms': 0.16885, 'vrms_to_vpp': 5.922416345869115},
    'DC': {'vpp_to_vrms': 1.0, 'vrms_to_vpp': 1.0}
}
_available_waves = ("SINe", "SQUare", "PULSe", "RAMP", "ARB", "NOISe", "DC")
_internal_arb_waves = [
    "AbsSine", "AmpALT", "AttALT", "Cardiac", "CosH", "EEG", "EOG", "GaussianMonopulse", "GaussPulse", "LogNormal",
    "Lorentz", "Pulseilogram", "Radar", "Sinc", "SineVer", "StairUD", "StepResp", "Trapezia", "TV", "VOICE",
    "Log_up", "Log_down", "Tri_up", "Tri_down"
]
_waves_min_max_freq = {
    "SINe": {
        "max_freq": 6e7,
        "min_freq": 1e-06
    },
    "SQUare": {
        "max_freq": 2e7,
        "min_freq": 1e-06
    },
    "PULSe": {
        "max_freq": 2e7,
        "min_freq": 1e-06
    },
    "RAMP": {
        "max_freq": 400000.0,
        "min_freq": 1e-06
    },
    "AbsSine": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "AmpALT": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "AttALT": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Cardiac": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "CosH": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "EEG": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "EOG": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "GaussianMonopulse": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "GaussPulse": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "LogNormal": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Lorentz": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Pulseilogram": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Radar": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Sinc": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "SineVer": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "StairUD": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "StepResp": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Trapezia": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "TV": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "VOICE": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Log_up": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Log_down": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Tri_up": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "Tri_down": {
        "max_freq": 1e7,
        "min_freq": 1e-06
    },
    "NOISe": {
        "max_freq": 1e-06,
        "min_freq": 1e-06
    },
    "DC": {
        "max_freq": 1e-06,
        "min_freq": 1e-06
    }
}


@pytest.fixture(scope="session")
def device():
    # TODO: Сделать проверку на ошибки при подключении
    address = "USB0::0x6656::0x0834::AWG1524090004::INSTR"
    dev = UTG900E(address)
    yield dev
    dev.close()


def test_limit_enable(device):
    print()
    set_param = ((1, False), (1, True), (2, False), (2, True))
    for channel, lim_en in set_param:
        device.limit_enable(channel, lim_en)
        get_lim_en = device.is_limit_enable(channel)
        assert lim_en == get_lim_en


def test_set_load(device):
    print()
    number_of_tests = 10
    random.seed(120)  # The fixed seed for reproducibility. Any number works
    set_param = \
        [
            {
                "channel": 1,
                "set_load": 0.2,
                "exp_load": 1,
            },
            {
                "channel": 2,
                "set_load": 10001,
                "exp_load": 10000,
            },
            {
                "channel": 1,
                "set_load": 50,
                "exp_load": 50,
            },
            {
                "channel": 2,
                "set_load": 10000,
                "exp_load": 10000,
            }
        ] + \
        [
            {
                "channel": random.randint(1, 2),
                "set_load": (val := random.randint(1, 9999)),
                "exp_load": val,
            } for __ in range(number_of_tests)
        ]
    for params in set_param:
        device.set_load(params["channel"], params["set_load"])
        get_load = device.get_load(params["channel"])
        assert get_load == params["exp_load"]


def test_set_lower_limit(device):
    print()
    number_of_tests = 1
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
        assert get_limit_v == expected_limit, \
            f"set_load: {set_load}\nset_limit: {set_limit}\nlower_limit: {lower_limit}\nupper_limit: {upper_limit}\n\
            expected_limit: {expected_limit}\nget_limit_v: {get_limit_v}\n"


def test_set_upper_limit(device):
    print()
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
    print()
    random.seed(100)
    set_param = [[random.randint(1, 2), wave] for wave in device._available_waves]
    for channel, set_wave in set_param:
        device.set_wave(channel, set_wave)
        get_wave = device.get_wave(channel)
        assert get_wave == set_wave


def test_set_frequency(device):
    print()
    number_of_tests = 30
    upper_limit = 6e7
    random.seed(200)  # The fixed seed for reproducibility. Any number works
    set_param = [
        {
            "channel": 1,
            "set_wave": random.choice(_available_waves),
            "set_arb_wave": random.choice(_internal_arb_waves),
            "set_freq": random.uniform(0, upper_limit),
        } for __ in range(number_of_tests)
    ]
    for test_number in range(len(set_param)):
        params = set_param[test_number]
        wave = params["set_wave"]
        device.set_wave(params["channel"], wave)
        if params["set_wave"] == "ARB":
            wave = params["set_arb_wave"]
            device.set_arb_wave(params["channel"], params["set_arb_wave"])
        device.set_frequency(params["channel"], int(params["set_freq"]))
        if params["set_freq"] > _waves_min_max_freq[wave]["max_freq"]:
            exp_freq = _waves_min_max_freq[wave]["max_freq"]
        elif params["set_freq"] < _waves_min_max_freq[wave]["min_freq"]:
            exp_freq = _waves_min_max_freq[wave]["min_freq"]
        else:
            exp_freq = int(params["set_freq"])
        get_freq = device.get_frequency(params["channel"])
        assert abs(float(get_freq) - exp_freq) <= 1e-06 * exp_freq, f"Test №: {test_number}. Get freq: {get_freq}. Params: {params}"


def test_set_period(device):
    print()
    number_of_tests = 20
    higher_value = 1e6
    lower_value = 1.7e-08
    random.seed(100)
    set_param = [[1, 0.9 * lower_value, lower_value], [1, 1.1 * higher_value, higher_value], [1, 0, lower_value]] + \
                [[
                    random.randint(1, 2),
                    set_val := random.uniform(0, 2e6),
                    set_val if lower_value <= set_val <= higher_value else (
                        higher_value if set_val > higher_value else lower_value)
                ] for __ in range(number_of_tests)]
    for channel, set_period, expected_period in set_param:
        device.set_wave(channel, "SINe")
        device.set_period(channel, set_period)
        get_period = device.get_period(channel)
        assert abs(get_period - expected_period) <= 1e-06 * expected_period


def test_set_phase(device):
    print()
    number_of_tests = 20
    higher_value = 360
    lower_value = -360
    random.seed(100)
    # channel, set_value, expected_value
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


def expected_amp_and_offset_calc(**kwargs) -> (float, float):
    upper_limit = _limit_calc(kwargs["load"]) if not kwargs["limit_enable"] else kwargs["upper_limit"]
    lower_limit = -1 * upper_limit if not kwargs["limit_enable"] else kwargs["lower_limit"]

    if kwargs["set_wave"] == "ARB":
        kwargs["set_wave"] = kwargs["set_arb_wave"]

    vrms_to_vpp_coefficient = _vpp_vrms_coeff_for_waves[kwargs["set_wave"]]["vrms_to_vpp"] if kwargs["set_unit"].upper() == "VRMS" else 1
    vpp_to_vrms_coefficient = _vpp_vrms_coeff_for_waves[kwargs["set_wave"]]["vpp_to_vrms"] if kwargs["set_unit"].upper() == "VRMS" else 1

    scope = upper_limit - lower_limit
    amplitude = scope if (amp := kwargs["set_amp"] * vrms_to_vpp_coefficient) > scope else amp

    if (val := upper_limit - 0.5 * amplitude) < 0: offset = val
    elif (val := lower_limit + 0.5 * amplitude) > 0: offset = val
    else: offset = 0

    amplitude *= vpp_to_vrms_coefficient

    # print("Offset: ", offset, _round_math(offset, 3))
    # print("Amplitude: ", amplitude, _truncate_decimal(amplitude, 3))

    return _truncate_decimal(amplitude, 3), _round_math(offset, 3)


def test_set_amplitude(device):
    print()
    number_of_tests = 100
    random.seed(100)

    set_param = \
    [
        {
            "channel": 1,
            "load": 1e4,
            "limit_enable": True,
            "lower_limit": -5,
            "upper_limit": 2,
            "set_wave": "SINe",
            "set_arb_wave": "AbsSine",
            "set_unit": "Vpp",
            "set_amp": 20,
        }
    ] +     \
    [
        {
            "channel": (channel := random.randint(1, 2)),
            "load": (load := random.randint(1, 9999)),
            "limit_enable": (limit_enable := bool(random.randint(0, 1))),
            "lower_limit": (lower_limit := _round_math(random.uniform(-10, 5), 3)),
            "upper_limit": (upper_limit := _round_math(random.uniform(lower_limit + 0.002, 10), 3)),
            "set_wave": (set_wave := random.choice(_available_waves[:-1])),
            "set_arb_wave": random.choice(_internal_arb_waves),
            "set_unit": (set_unit := random.choice(("Vpp", "Vrms"))),
            "set_amp": (set_amp := _round_math(random.uniform(0, 21), 3)),
        } for __ in range(number_of_tests)
    ]

    for test_number in range(len(set_param)):
        # if test_number != 1:
        #     continue
        params = set_param[test_number]
        device.set_load(params["channel"], params["load"])
        device.limit_enable(params["channel"], params["limit_enable"])
        device.set_lower_limit(params["channel"], params["lower_limit"])
        device.set_upper_limit(params["channel"], params["upper_limit"])
        device.set_wave(params["channel"], params["set_wave"])
        if params["set_wave"] == "ARB":
            device.set_arb_wave(params["channel"], params["set_arb_wave"])
        device.set_amplitude_unit(params["channel"], params["set_unit"])
        device.set_amplitude(params["channel"], params["set_amp"])
        get_amplitude = device.get_amplitude(params["channel"])
        get_offset = device.get_offset(params["channel"])
        exp_amp, exp_offset = expected_amp_and_offset_calc(
            load=params["load"],
            limit_enable=params["limit_enable"],
            lower_limit=device.get_lower_limit(params["channel"]),
            upper_limit=device.get_upper_limit(params["channel"]),
            set_wave=params["set_wave"],
            set_arb_wave=params["set_arb_wave"],
            set_unit=params["set_unit"],
            set_amp=params["set_amp"]
        )
        # print(device.get_offset(params["channel"]))
        # assert (get_amplitude, get_offset) == (exp_amp, exp_offset), f"Test №{test_number}. Context: {params}"
        assert _round_math(abs(get_amplitude - exp_amp), 3) <= 0.001, f"Test №{test_number}. Context: {params}"# and abs(get_offset - exp_offset) <= 0.001
        assert _round_math(abs(get_offset - exp_offset), 3) <= 0.001, f"Test №{test_number}. Context: {params}.\nget_offset: {get_offset}, exp_offset: {exp_offset}"


    # a = {"SINe": [10, 3.536], "SQUare": [10, 5], "PULSe": [10, 5], "RAMP": [10, 2.887], "NOIse": [10, 5]}
    # vpp_vrms_coeff_for_waves = {
    #     'SINe': [0.35355, 2.8284542497525105], 'SQUare': [0.5, 2.0], 'PULSe': [0.5, 2.0],
    #     'RAMP': [0.2887, 3.4638032559750607], 'AbsSine': [0.5, 2.0], 'AmpALT': [0.5, 2.0], 'AttALT': [0.5, 2.0],
    #     'Cardiac': [0.5, 2.0], 'CosH': [0.3323, 3.009328919650918], 'EEG': [0.15025, 6.655574043261232],
    #     'EOG': [0.1407, 7.107320540156361], 'GaussianMonopulse': [0.36920000000000003, 2.7085590465872156],
    #     'GaussPulse': [0.39275000000000004, 2.546148949713558], 'LogNormal': [0.1765, 5.6657223796034],
    #     'Lorentz': [0.15489999999999998, 6.45577792123951], 'Pulseilogram': [0.27080000000000004, 3.692762186115214],
    #     'Radar': [0.4473, 2.23563603845294], 'Sinc': [0.3806, 2.627430373095113], 'SineVer': [0.4667, 2.142704092564817],
    #     'StairUD': [0.31675, 3.1570639305445933], 'StepResp': [0.45095, 2.2175407473112316],
    #     'Trapezia': [0.32475, 3.079291762894534], 'TV': [0.25070000000000003, 3.9888312724371757],
    #     'VOICE': [0.3227, 3.098853424233034], 'Log_up': [0.4157, 2.405580947798893],
    #     'Log_down': [0.37985, 2.6326181387389758], 'Tri_up': [0.40225, 2.4860161591050343],
    #     'Tri_down': [0.16885, 5.922416345869115], 'NOISe': [0.16885, 5.922416345869115], 'DC': [1.0, 1.0]
    # }
    #
    # print()
    # # for wave in vpp_vrms_coeff_for_waves:
    # #     i, j = vpp_vrms_coeff_for_waves[wave]
    # #     print(f"{wave:<20}: 20 Vpp = {round(20 * i, 4)} Vrms")
    # # for val in a:
    # #     vpp, vrms = a[val]
    # #     k = vrms / vpp
    # #     print(val, [vpp, vrms, k])
    # # device.limit_enable(1, False)
    # # device.set_wave(1, "arb")
    # # device.set_arb_source(1, "internal")
    # # device.set_arb_wave(1, "AttALT")
    # # device.set_amplitude_unit(1, "Vrms")
    # # device.set_amplitude(1, 11)
    # pass


# def test_get_waves_freq(device):
#     print()
#     _waves_freq = {}
#     for wave in _available_waves:
#         device.set_wave(1, wave)
#         if wave == "ARB":
#             for wave_file in _internal_arb_waves:
#                 device.set_arb_wave(1, wave_file)
#                 device.set_frequency(1, 1e8)
#                 max_freq = device.get_frequency(1)
#                 device.set_frequency(1, 1e-8)
#                 min_freq = device.get_frequency(1)
#                 _waves_freq[wave_file] = {"max_freq": max_freq, "min_freq": min_freq}
#
#         else:
#             device.set_frequency(1, 1e8)
#             max_freq = device.get_frequency(1)
#             device.set_frequency(1, 1e-8)
#             min_freq = device.get_frequency(1)
#             _waves_freq[wave] = {"max_freq": max_freq, "min_freq": min_freq}
#
#     print(_waves_freq)
#     print(json.dumps({'SINe': {'max_freq': 60000000.0, 'min_freq': 1e-06}, 'SQUare': {'max_freq': 20000000.0, 'min_freq': 1e-06}, 'PULSe': {'max_freq': 20000000.0, 'min_freq': 1e-06}, 'RAMP': {'max_freq': 400000.0, 'min_freq': 1e-06}, 'AbsSine': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'AmpALT': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'AttALT': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Cardiac': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'CosH': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'EEG': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'EOG': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'GaussianMonopulse': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'GaussPulse': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'LogNormal': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Lorentz': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Pulseilogram': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Radar': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Sinc': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'SineVer': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'StairUD': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'StepResp': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Trapezia': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'TV': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'VOICE': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Log_up': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Log_down': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Tri_up': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'Tri_down': {'max_freq': 10000000.0, 'min_freq': 1e-06}, 'NOISe': {'max_freq': 1e-06, 'min_freq': 1e-06}, 'DC': {'max_freq': 1e-06, 'min_freq': 1e-06}}, indent=4))


# def test_test1(device):
#     print()
#     arb_waves = (
#         "AbsSine", "AmpALT", "AttALT", "Cardiac", "CosH", "EEG", "EOG", "GaussianMonopulse", "GaussPulse", "LogNormal",
#         "Lorentz", "Pulseilogram", "Radar", "Sinc", "SineVer", "StairUD", "StepResp", "Trapezia", "TV", "VOICE",
#         "Log_up", "Log_down", "Tri_up", "Tri_down"
#     )
#     arb_waves_indexes = dict(zip(arb_waves, [i for i in range(24)]))
#     print()
#     print(arb_waves_indexes)
#     print(arb_waves.index("Sinc"))
#     print(arb_waves[13])
#     pass


# def test_test(device):
#     print()
#     waves = ("SINe", "SQUare", "PULSe", "RAMP", "ARB", "NOISe", "DC")
#     vpp_to_vrms_coeff_for_waves = {}
#     arb_waves = (
#         "AbsSine", "AmpALT", "AttALT", "Cardiac", "CosH", "EEG", "EOG", "GaussianMonopulse", "GaussPulse", "LogNormal",
#         "Lorentz", "Pulseilogram", "Radar", "Sinc", "SineVer", "StairUD", "StepResp", "Trapezia", "TV", "VOICE",
#         "Log_up", "Log_down", "Tri_up", "Tri_down"
#     )
#     # wave_names = []
#     # amps = []
#
#     for wave in waves:
#         if wave == "ARB":
#             device.set_wave(1, wave)
#             for wave_file in arb_waves:
#                 device.set_arb_source(1, "INTernal")
#                 device.set_arb_wave(1, wave_file)
#                 device.set_amplitude_unit(1, "Vpp")
#                 device.set_amplitude(1, 20)
#                 device.set_amplitude_unit(1, "Vrms")
#                 amp = device.get_amplitude(1)
#                 wave_name = device.get_arb_wave(1).upper()
#                 vpp_to_vrms_coeff_for_waves[wave_name] = {"vpp_to_vrms": amp / 20, "vrms_to_vpp": 20 / amp}
#         else:
#             device.set_wave(1, wave)
#             device.set_amplitude_unit(1, "Vpp")
#             device.set_amplitude(1, 20)
#             device.set_amplitude_unit(1, "Vrms")
#             amp = device.get_amplitude(1)
#             wave_name = device.get_wave(1).upper()
#             vpp_to_vrms_coeff_for_waves[wave_name] = {"vpp_to_vrms": amp / 20, "vrms_to_vpp": 20 / amp}
#
#     print()
#     print(vpp_to_vrms_coeff_for_waves)
#     print(json.dumps(vpp_to_vrms_coeff_for_waves, indent=4))
#
