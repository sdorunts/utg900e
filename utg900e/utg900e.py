import pyvisa
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UTG900E:
    _channel_numbers = (1, 2)
    _available_amplitude_units = ("VPP", "VRMS")
    _available_modes = ("CONTINUE", "AM", "PM", "FM", "FSK", "Line", "Log")
    _available_waves = ("SINE", "SQUARE", "PULSE", "RAMP", "ARB", "NOISE", "DC")
    _available_arb_sources = ("INTERNAL", "EXTERNAL")
    _internal_arb_waves = (
        "AbsSine", "AmpALT", "AttALT", "Cardiac", "CosH", "EEG", "EOG", "GaussianMonopulse", "GaussPulse", "LogNormal",
        "Lorentz", "Pulseilogram", "Radar", "Sinc", "SineVer", "StairUD", "StepResp", "Trapezia", "TV", "VOICE",
        "Log_up", "Log_down", "Tri_up", "Tri_down"
    )
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

    def __init__(self, device_addr=None):
        self.rm = pyvisa.ResourceManager()
        self.inst = None
        self._limit_calc = lambda x: 10 if x == 10000 else self._round_math(10 * x / (50 + x), 3)
        self._round_math = lambda number, digits=0: float(Decimal(str(number)).quantize(Decimal(f"1e-{digits}"), rounding=ROUND_HALF_UP))
        self._truncate_decimal = lambda number, digits=0: float(Decimal(str(number)).quantize(Decimal(f"1e-{digits}"), rounding=ROUND_DOWN))
        if device_addr:
            self.connect(device_addr)
        else:
            logger.warning("Device has not been connected: address hasn't been provided.")

    def connect(self, device_addr):
        try:
            self.inst = self.rm.open_resource(device_addr)
            logger.info(f"Connected to {device_addr}")
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise

    def close(self):
        if self.inst:
            self.inst.close()
            logger.info("Connection closed.")

    def write(self, command):
        logger.debug(f"→ {command}")
        self.inst.write(command)

    def query(self, command):
        logger.debug(f"→ {command}")
        return self.inst.query(command)

    def identify(self):
        return self.query("*IDN?")

    def reset(self):
        self.write("*RST")

    # --- Low-level commands (SCPI wrappers) ---

    def set_output(self, channel: int, state=True):
        """
         Function
            Set the specified channel output ON/OFF
         Example
            gen.set_output(1) - Set the channel 1 output ON
            gen.set_output(1, False) - Set the channel 1 output OFF

        :param channel: Channel No. Value 1, 2
        :param state: Channels output state. False in OFF, True in ON
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if type(state) is not bool:
            raise TypeError(f"{bool} was expected as state type, instead {type(state)} has been provided")
        self.write(f":CHANnel{channel}:OUTPut {'ON' if state else 'OFF'}")


    def get_output(self, channel: int) -> int:
        """
         Function
            Get the specified channel output status
         Example
            gen.get_output(1) - Returns 0 or 1

        :param channel: Channel No. Value 1, 2
        :return: Specified channel output status. 0 in OFF, 1 in ON
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:OUTPut?")


    def set_inversion(self, channel: int, inversion=True) -> None:
        """
         Function
            Set the specified channel reverse
         Example
            gen.set_inversion(1, True) - Set the reverse output of channel 1 ON

        :param channel: Channel No. Value 1, 2
        :param inversion: Revers of the specified channel. True in ON, False in OFF
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if type(inversion) is not bool:
            raise TypeError(f"{bool} was expected as inversion type, instead {type(inversion)} has been provided")
        self.write(f":CHANnel{channel}:INVersion {"ON" if inversion else "OFF"}")


    def get_inversion(self, channel: int) -> int:
        """
         Function
            Get the specified channel reverse
         Example
            gen.get_inversion(1) - Returns 0 or 1

        :param channel: Channel No. Value 1, 2
        :return: The specified channel reverse. 0 in OFF, 1 in ON
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:INVersion?")


    def set_sync(self, channel: int, sync=False) -> None:
        """
         Function
            Set the sync output of channel.
         Example
            gen.set_sync(1, True) - Set the sync output of channel 1 ON

        :param channel: Channel No. Value 1, 2
        :param sync: Sync output of channel. 0 in OFF, 1 in ON. Only one sync output interface in the device, and can only open the sync output of one channel.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if type(sync) is not bool:
            raise TypeError(f"{bool} was expected as sync type, instead {type(sync)} has been provided")
        self.write(f":CHANnel{channel}:OUTPut:SYNC {"ON" if sync else "OFF"}")


    def get_sync(self, channel: int) -> int:
        """
         Function
            Get the sync output of specified channel.
         Example
            gen.get_sync(1) - Returns 0 or 1

        :param channel: Channel No. Value 1, 2
        :return: The sync output of specified channel. 0 in OFF, 1 in ON.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:OUTPut:SYNC?")


    def limit_enable(self, channel: int, enable=True) -> None:
        """
         Function
            Set the amplitude limiting ON/OFF of specified channel.
         Example
            gen.limit_enable(1) - Set the amplitude limiting of channel 1 ON

        :param channel: Channel No. Value 1, 2
        :param enable: Enable or disable limiting. 0 in OFF, 1 in ON.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if type(enable) is not bool:
            raise TypeError(f"{bool} was expected as enable type, instead {type(enable)} has been provided")
        self.write(f":CHANnel{channel}:LIMit:ENABle {"ON" if enable else "OFF"}")


    def is_limit_enable(self, channel: int) -> int:
        """
         Function
            Get the amplitude limiting status of specified channel.
         Example
            gen.is_limit_enable(1) - Returns 0 or 1

        :param channel: Channel No. Value 1, 2
        :return: The amplitude limiting status of specified channel. 0 in OFF, 1 in ON.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return int(self.query(f":CHANnel{channel}:LIMit:ENABle?"))


    def set_lower_limit(self, channel: int, limit_v: float) -> None:
        """
         Function
            Set the lower amplitude limit of specified channel.
         Example
            get.set_lower_limit(1, 2) - Set the lower amplitude limit of channel 1 to 2V

        :param channel: Channel No. Value 1, 2
        :param limit_v: Voltage in Volts as a float number. Range -10V~9.998V. Its unit is the specified unit of current channel.
        :return: None
        """
        load = self.get_load(channel)
        upper_limit = 10 if load == 10000 else round(10 * load / (50 + load), 3)
        lower_limit = -1 * upper_limit
        logger.info(f"Load: {load}, upper_limit: {upper_limit}, lower_limit: {lower_limit}")
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided.")
        if limit_v < lower_limit:
            logger.info(f"Try to set {limit_v}V as lower limit, but it can not be lower than {lower_limit}V. Lower limit set to {lower_limit}V.")
            limit_v = lower_limit
        elif limit_v >= upper_limit:
            logger.info(f"Try to set {limit_v}V as lower limit, but it can not be greater or equal to {upper_limit}V. Lower limit set to {upper_limit}V.")
            limit_v = upper_limit
        self.write(f":CHANnel{channel}:LIMit:LOWer {limit_v}")


    def get_lower_limit(self, channel: int) -> float:
        """
         Function
            Get the lower amplitude limit of specified channel.
         Example
            get.get_lower_limit(1) - Returns lower amplitude limit of channel 1

        :param channel: Channel No. Value 1, 2
        :return: The lower limit voltage in Volts as a float number.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return round(float(self.query(f":CHANnel{channel}:LIMit:LOWer?")), 3)


    def set_upper_limit(self, channel: int, limit_v: float) -> None:
        """
         Function
            Set the upper amplitude limit of specified channel.
         Example
            get.set_upper_limit(1, 2) - Set the upper amplitude limit of channel 1 to 2V

        :param channel: Channel No. Value 1, 2
        :param limit_v: Voltage in Volts as a float number. Range -9.998V~10V. Its unit is the specified unit of current channel.
        :return: None
        """
        load = self.get_load(channel)
        upper_limit = self._limit_calc(load)
        # upper_limit = 10 if load == 10000 else round(10 * load / (50 + load), 3)
        lower_limit = -1 * upper_limit
        logger.info(f"Load: {load}, upper_limit: {upper_limit}, lower_limit: {lower_limit}")
        # lower_limit = round(self.get_lower_limit(channel), 3)
        # upper_limit = round(self.get_upper_limit(channel), 3)
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided.")
        if limit_v <= lower_limit:
            logger.info(f"Try to set {limit_v}V as upper limit, but it can not be lower or equal to {lower_limit}V. Upper limit set to {lower_limit}V.")
            limit_v = lower_limit
        elif limit_v > upper_limit:
            logger.info(f"Try to set {limit_v}V as upper limit, but it can not be greater than {upper_limit}V. Upper limit set to {upper_limit}V.")
            limit_v = upper_limit
        self.write(f":CHANnel{channel}:LIMit:UPPer {limit_v}")


    def get_upper_limit(self, channel: int) -> float:
        """
         Function
            Get the upper amplitude limit of specified channel.
         Example
            get.get_upper_limit(1) - Returns upper amplitude limit of channel 1

        :param channel: Channel No. Value 1, 2.
        :return: The upper limit voltage in Volts as a float number.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided.")
        return float(self.query(f":CHANnel{channel}:LIMit:UPPer?"))


    def set_amplitude_unit(self, channel: int, unit="VPP") -> None:
        """
         Function
            Set the unit of output amplitude in specified channel.
         Example
            gen.set_amplitude_unit(1, "Vrms") - Set the unit of output amplitude in channel 1 to VRMS

        :param channel: Channel No. Value 1, 2.
        :param unit: The unit of output amplitude in specified channel. Available units are VPP and VRMS.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        unit = unit.upper()
        if unit not in self._available_amplitude_units:
            raise ValueError(f"Unit value should be in {self._available_amplitude_units}, instead value {unit} has been provided")
        self.write(f":CHANnel{channel}:AMPLitude:UNIT {unit}")


    def get_amplitude_unit(self, channel: int) -> str:
        """
         Function
            Get the unit of output amplitude in specified channel.
         Example
            gen.get_amplitude_unit(1) - Get the unit of output amplitude in channel 1

        :param channel: Channel No. Value 1, 2.
        :return: The unit of output amplitude in required channel as string.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:AMPLitude:UNIT?")


    def set_load(self, channel: int, resistance_r=50) -> None:
        """
         Function
            Set the output load of specified channel.
         Example
            gen.set_load(1, 50) - Set the output load of channel 1 to 50Ω

        :param channel: Channel No. Value 1, 2.
        :param resistance_r: Load resistance, in "Ω". The resistance value should be within the range of 1~10000, and the 10000 is for high resistance.
        :return: None
        """
        lower_resistance = 1
        higher_resistance = 1e4
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided.")
        if resistance_r < lower_resistance:
            logger.info(f"Try to set {resistance_r} as current load, but it can not be lower than 1Ω. Resistance set to 1Ω.")
        elif resistance_r > higher_resistance:
            logger.info(f"Try to set {resistance_r} as current load, but it can not be grater than 10000Ω. Resistance set to 10000Ω.")
        self.write(f":CHANnel{channel}:LOAD {resistance_r}")
        lower_limit = round(self.get_lower_limit(channel), 3)
        upper_limit = round(self.get_upper_limit(channel), 3)
        logger.info(f"Load changed to {resistance_r}. Lower limit and upper limit equals to {lower_limit}V and {upper_limit}V respectively.")


    def get_load(self, channel: int) -> float:
        """
         Function
            Get the output load of specified channel.
         Example
            gen.get_load(1) - Get the output load of channel 1

        :param channel: Channel No. Value 1, 2.
        :return: The load resistance of specified channel as a float number.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided.")
        return float(self.query(f":CHANnel{channel}:LOAD?"))


    def set_wave(self, channel: int, wave: str) -> None:
        """
         Function
            Set the fundamental wave types of specified channel.
         Example
            gen.set_wave(1, "PULSE") - Set the channel 1 to pulse wave

        :param channel: Channel No. Value 1, 2.
        :param wave: Fundamental wave types, including Sine, Square, Pulse, Ramp, Arbitrary, Noise and DC.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided.")
        wave = wave.upper()
        if wave not in self._available_waves:
            raise ValueError(f"Wave should be in available waves: {self._available_waves}.")
        self.write(f":CHANnel{channel}:BASE:WAVe {wave}")


    def get_wave(self, channel: int) -> str:
        """
         Function
            Get the fundamental wave types of specified channel.
         Example
            gen.get_wave(1) - Get the channel 1 wave

        :param channel: Channel No. Value 1, 2.
        :return: Fundamental wave types of specified channel. "SINe", "PULse", etc.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:BASE:WAVe?")


    def set_frequency(self, channel: int, freq_hz: float) -> None:
        """
         Function
            Set the output frequency of specified channel.
         Example
            gen.set_frequency(1, 2000) - Set the output frequency of channel 1 to 2KHz

        :param channel: Channel No. Value 1, 2.
        :param freq_hz: Frequency value, in 'Hz' unit. (1e-6s ~ current max. frequency of wave).
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        self.write(f":CHANnel{channel}:BASE:FREQuency {freq_hz}")


    def get_frequency(self, channel: int):
        """
         Function
            Get the output frequency of specified channel.
         Example
            gen.get_frequency(1) - Get the output frequency of channel 1

        :param channel: Channel No. Value 1, 2.
        :return: Modulated frequency of specified channel signal in 'Hz' as a float number.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return float(self.query(f":CHANnel{channel}:BASE:FREQuency?"))


    def set_period(self, channel: int, period_s: float):
        """
         Function
            Set the output period of specified channel
         Example
            gen.set_period(1, 0.002) - Set the output period of channel 1 to 2ms

        :param channel: Channel No. Value 1, 2
        :param period_s: Period, in “s” unit. If sine wave: max. ~ 1e3s
        :return: None
        """
        higher_value = 1e6
        lower_value = 1.7e-08
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if period_s > higher_value:
            logger.info(f"Try to set {period_s}V as a period, but it can not grater than {higher_value}V. Period set to {higher_value}V.")
            period_s = higher_value
        elif period_s < lower_value:
            logger.info(f"Try to set {period_s}V as a period, but it can not lower than {lower_value}V. Period set to {lower_value}V.")
            period_s = lower_value
        self.write(f":CHANnel{channel}:BASE:PERiod {period_s}")


    def get_period(self, channel: int) -> float:
        """
         Function
            Get the period of specified channel.
         Example
            gen.get_period(1) - Returns period in seconds

        :param channel: Channel No. Value 1, 2
        :return: Period of specified channel, using scientific notation to return.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return float(self.query(f":CHANnel{channel}:BASE:PERiod?"))


    def set_phase(self, channel: int, phase_deg: float) -> None:
        """
         Function
            Set the output phase of specified channel.
         Example
            gen.set_phase(1, 20) - Set the output phase of channel 1 to 20°

        :param channel: Channel No. Value 1, 2.
        :param phase_deg: The phase, in “°” unit, range of -360~360.
        :return: None
        """
        max_phase_deg = 360
        min_phase_deg = -360
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if phase_deg > max_phase_deg:
            logger.info(f"Try to set {phase_deg}V as a phase, but it can not grater than {max_phase_deg}V. Phase set to {max_phase_deg}V.")
            phase_deg = max_phase_deg
        if phase_deg < min_phase_deg:
            logger.info(f"Try to set {phase_deg}V as a phase, but it can not lower than {min_phase_deg}V. Phase set to {min_phase_deg}V.")
            phase_deg = min_phase_deg
        self.write(f":CHANnel{channel}:BASE:PHAse {phase_deg}")


    def get_phase(self, channel: int) -> float:
        """
         Function
            Get the output phase of specified channel.
         Example
            gen.get_phase(1) - Get the output phase of channel 1

        :param channel: Channel No. Value 1, 2.
        :return: Output phase of specified channel as a float number in “°” unit, range of -360~360.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return round(float(self.query(f":CHANnel{channel}:BASE:PHAse?")), 2)


    def set_amplitude(self, channel: int, amplitude_v: float) -> None:
        """
         Function
            Set the output amplitude of specified channel.
         Example
            gen.set_amplitude(1, 2) - Set the output amplitude of channel 1 to 2V

        :param channel: Channel No. Value 1, 2.
        :param amplitude_v: Voltage in Volts. Unit is the specified one of current channel. 1mVpp ~ is the max.output in the current load condition. When the current unit is VPP, the current max.load=current load*20/(50+current load)
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")

        amp_unit = self.get_amplitude_unit(channel)
        wave = self.get_wave(channel)
        if wave == "ARB":
            wave = self.get_arb_wave(channel)
        vrms_to_vpp_coefficient = self._vpp_vrms_coeff_for_waves[wave]["vrms_to_vpp"] if amp_unit == "VRMS" else 1
        vpp_to_vrms_coefficient = self._vpp_vrms_coeff_for_waves[wave]["vpp_to_vrms"] if amp_unit == "VRMS" else 1

        if self.is_limit_enable(channel):
            upper_limit = self.get_upper_limit(channel)
            lower_limit = self.get_lower_limit(channel)
        else:
            load = self.get_load(channel)
            upper_limit = self._limit_calc(load)
            lower_limit = -1 * upper_limit

        scope = upper_limit - lower_limit
        amplitude_v *= vrms_to_vpp_coefficient
        if amplitude_v > scope:
            logger.info(f"Amplitude value is out of range. Amplitude set to {scope * vpp_to_vrms_coefficient}V.")
            amplitude_v = scope

        offset = 0
        high = 0.5 * amplitude_v
        low = -0.5 * amplitude_v
        if (val := upper_limit - high) < 0:
            offset = val
        elif (val := lower_limit - low) > 0:
            offset = val
        self.set_offset(channel, offset)
        amplitude_v *= vpp_to_vrms_coefficient

        self.write(f":CHANnel{channel}:BASE:AMPLitude {amplitude_v}")


    def get_amplitude(self, channel: int) -> float:
        """
         Function
            Get the output amplitude of specified channel.
         Example
            gen.get_amplitude(1) - Get the output amplitude of channel 1

        :param channel: Channel No. Value 1, 2.
        :return: Output amplitude of specified channel as a float number.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return float(self.query(f":CHANnel{channel}:BASE:AMPLitude?"))


    def set_offset(self, channel: int, offset_v: float):
        """
         Function
            Set the DC output offset of specified channel.
         Example
            gen.set_offset(1, 2) - Set the DC output offset of channel 1 to 2V

        Max.DC of current load = (current load)*10/(50 + current load)-(current min.AC)/2.
        Min.AC is 2mVpp, value 0 in DC mode

        :param channel: Channel No. Value 1, 2.
        :param offset_v: Voltage, in "V" unit. Range of 0~±max.DC of current load.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        self.write(f":CHANnel{channel}:BASE:OFFSet {offset_v}")


    def get_offset(self, channel: int) -> float:
        """
         Function
            Get the DC output offset of specified channel.
         Example
            gen.get_offset(1) - Get the DC output offset of channel 1

        :param channel: Channel No. Value 1, 2.
        :return: DC output offset of specified channel as a float number in "V" unit.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:BASE:OFFSet?")


    def set_high(self, channel: int, high_v: float) -> None:
        """
         Function
            Set the high signal output value of specified channel.
         Example
            gen.set_high(1, 2) - Set the high signal output value of channel 1 to 2V

        :param channel: Channel No. Value 1, 2.
        :param high_v: Voltage, in "V" unit.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        self.write(f":CHANnel{channel}:BASE:HIGH {high_v}")


    def get_high(self, channel: int) -> float:
        """
         Function
            Get the high signal output value of specified channel.
         Example
            gen.get_high(1) - Get the high signal output value of channel 1.

        :param channel: Channel No. Value 1, 2.
        :return: High signal output value of specified channel as a float number.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:BASE:HIGH?")


    def set_low(self, channel: int, low_v: float) -> None:
        """
         Function
            Set the low signal output value of specified channel.
         Example
            gen.set_low(1, 2) - Set the low signal output value of channel 1 to 2V

        :param channel: Channel No. Value 1, 2.
        :param low_v: Voltage, in "V" unit.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        self.write(f":CHANnel{channel}:BASE:LOW {low_v}")


    def get_low(self, channel: int) -> float:
        """
         Function
            Get the low signal output value of specified channel.
         Example
            gen.get_low(1) - Get the low signal output value of channel 1.

        :param channel: Channel No. Value 1, 2.
        :return: Low signal output value of specified channel as a float number.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:BASE:LOW?")


    def set_duty(self, channel: int, duty_percent: float) -> None:
        """
         Function
            Set the duty ratio of signal output in specified channel.
         Example
            gen.set_duty(1, 20) - Set the duty ratio of signal output in channel 1 to 20%

        :param channel: Channel No. Value 1, 2.
        :param duty_percent: Duty ratio, in “%” unit, range of 0~100.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if not (0 <= duty_percent <= 100):
            raise ValueError("Duty must be 0–100%")
        self.write(f":CHANnel{channel}:BASE:DUTY {duty_percent}")


    def get_duty(self, channel: int) -> float:
        """
         Function
            Get the duty ratio of signal output in specified channel.
         Example
            gen.get_duty(1, 20) - Get the duty ratio of signal output in channel 1

        :param channel: Channel No. Value 1, 2.
        :return: Duty ratio of signal output in specified channel in "%" unit.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:BASE:DUTY?")


    def set_symmetry(self, channel: int, symmetry_percent: float) -> None:
        """
         Function
            Set the signal output symmetry of ramp wave in specified channel.
         Example
            gen.set_symmetry(1, 20) - Set the ramp wave signal symmetry of channel 1 to 20%

        :param channel: Channel No. Value 1, 2.
        :param symmetry_percent: Symmetry, in “%” unit, range of 0~100.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if not (0 <= symmetry_percent <= 100):
            raise ValueError("Symmetry must be 0–100%")
        self.write(f":CHANnel{channel}:RAMP:SYMMetry {symmetry_percent}")


    def get_symmetry(self, channel: int) -> float:
        """
         Function
            Get the signal output symmetry of ramp wave in specified channel.
         Example
            gen.get_symmetry(1, 20) - Get the ramp wave signal symmetry of channel 1

        :param channel: Channel No. Value 1, 2.
        :return: Signal output symmetry of ramp wave in specified channel in percents.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:RAMP:SYMMetry?")


    def set_rise_time(self, channel: int, rise_s: float) -> None:
        """
         Function
            Set the rising edge pulse width of signal pulse wave in specified channel.
         Example
            gen.set_rise_time(1, 0.002) - Set the rising edge pulse width of channel 1 signal to 2ms.

        :param channel: Channel No. Value 1, 2.
        :param rise_s: Rising edge pulse width, in “S” unit.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        self.write(f":CHANnel{channel}:PULSe:RISe {rise_s}")


    def get_rise_time(self, channel: int) -> float:
        """
         Function
            Get the rising edge pulse width of signal pulse wave in specified channel.
         Example
            gen.get_rise_time(1) - Get the rising edge pulse width of channel 1 signal.

        :param channel: Channel No. Value 1, 2.
        :return: Rising edge pulse width of signal pulse wave in specified channel as a float number in seconds.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:PULSe:RISe?")


    def set_fall_time(self, channel: int, fall_s: float) -> None:
        """
         Function
            Set the falling edge pulse width of signal pulse wave in specified channel.
         Example
            gen.set_fall_time(1, 0.002) - Set the falling edge pulse width of channel 1 signal to 2ms.

        :param channel: Channel No. Value 1, 2.
        :param fall_s: Falling edge pulse width, in “S” unit.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        self.write(f":CHANnel{channel}:PULSe:FALL {fall_s}")


    def get_fall_time(self, channel: int) -> float:
        """
         Function
            Get the falling edge pulse width of signal pulse wave in specified channel.
         Example
            gen.get_fall_time(1, 0.002) - Get the falling edge pulse width of channel 1 signal to 2ms.

        :param channel: Channel No. Value 1, 2.
        :return: Falling edge pulse width of signal pulse wave in specified channel as a float number in seconds.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:PULSe:FALL?")


    def set_mode(self, channel: int, mode: str) -> None:
        """
         Function
            Set the signal types of specified channel, CONTINUE, AM, PM, FM, FSK, Line, Log.
         Example
            gen.set_mode(1, "AM") - Set the channel 1 signal to AM.

        :param channel: Channel No. Value 1, 2.
        :param mode: Mode of signal in specified channel.
        :return: None
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        self.write(f":CHANnel{channel}:MODe {mode.upper()}")


    def get_mode(self, channel: int) -> str:
        """
         Function
            Get the signal types of specified channel, CONTINUE, AM, PM, FM, FSK, Line, Log.
         Example
            gen.get_mode(1) - Get the channel 1 signal.

        :param channel: Channel No. Value 1, 2.
        :return: Signal types of specified channel.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:MODe?")


    def set_arb_source(self, channel: int, source="INTernal") -> None:
        """
         Function
            Set the arbitrary wave source of specified channel.
         Example
            gen.set_arb_source(1, "EXTernal") - Set the arbitrary wave source of channel 1 to be external.

        :param channel: Channel No. Value 1, 2.
        :param source: Arbitrary wave source of specified channel, Internal and External.
        :return: None
        """
        source = source.upper()
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if source not in self._available_arb_sources:
            raise ValueError(f"Arb source should be in {self._available_arb_sources}, instead '{source}' has been provided")
        self.write(f":CHANnel{channel}:ARB:SOURce {source}")


    def get_arb_source(self, channel: int) -> str:
        """
         Function
            Get the arbitrary wave source of specified channel.
         Example
            gen.get_arb_source(1) - Get the arbitrary wave source of channel 1.

        :param channel: Channel No. Value 1, 2.
        :return: Returns arb wave source. INTernal or EXTernal
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self.query(f":CHANnel{channel}:ARB:SOURce?")


    def set_arb_wave(self, channel: int, wave: str) -> None:
        """
         Function
            Set the specified arb wave using available waves.
         Example
            gen.set_arb_wave(1, "Radar") - Set the channel 1 to load the arbitrary wave Radar, stored in signal source.

        List of available waves:
        "AbsSine", "AmpALT", "AttALT", "Cardiac", "CosH", "EEG", "EOG", "GaussianMonopulse", "GaussPulse", "LogNormal",
        "Lorentz", "Pulseilogram", "Radar", "Sinc", "SineVer", "StairUD", "StepResp", "Trapezia", "TV", "VOICE",
        "Log_up", "Log_down", "Tri_up", "Tri_down"

        :param channel: Channel No. Value 1, 2.
        :param wave: Arbitrary wave stored in signal source. Available waves are shown above.
        :return: None.
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        if wave not in self._internal_arb_waves:
            raise ValueError()
        self.write(f":CHANnel{channel}:ARB:INDex {self._internal_arb_waves.index(wave)}")


    def get_arb_wave(self, channel: int) -> str:
        """
        :param channel:
        :return:
        """
        if channel not in self._channel_numbers:
            raise ValueError(f"Channel value should be in {self._channel_numbers}, instead value {channel} has been provided")
        return self._internal_arb_waves[int(float(self.query(f":CHANnel{channel}:ARB:INDex?")))]


    # --- Universal signal setting methods ---

    def configure_waveform(self, channel: int, waveform="SINE", mode="CONTinue", **kwargs):
        """
        Universal signal configurator

        Examples of parameters in **kwargs:
        - freq (Hz)
        - amplitude (V)
        - offset (V)
        - phase (deg)
        - duty (%, only for SQUARE and PULSE)
        - symmetry (%, for RAMP only)
        - rise_time (s, for PULSE only)
        - fall_time (s, for PULSE only)Low-level commands
        """
        min_ac_div2_v= 0.001
        wave = waveform.upper()

        self.set_mode(channel, mode)
        self.set_wave(channel, wave)

        if wave == "ARB":
            if "arb_source" in kwargs:
                self.set_arb_source(channel, kwargs["arb_source"])
            if "wave_file" in kwargs:
                self.set_arb_wave(channel, kwargs["wave_file"])

        if "dc" in kwargs:
            self.set_low(channel, kwargs["dc"] - min_ac_div2_v)
            self.set_high(channel, kwargs["dc"] + min_ac_div2_v)

        if "freq" in kwargs and "period" in kwargs:
            raise ValueError("")
        elif "freq" in kwargs:
            self.set_frequency(channel, kwargs["freq"])
        elif "period" in kwargs:
            self.set_period(channel, kwargs["period"])

        if "amp_unit" in kwargs or "amp" in kwargs or "offset" in kwargs:
            if ("high" in kwargs or "low" in kwargs) and (wave != "DC"):
                raise ValueError("Parameters 'high' and 'low' shouldn't be used together with 'amp_unit', 'amp' and 'offset' parameters")
            if "amp_unit" in kwargs:
                self.set_amplitude_unit(channel, kwargs["amp_unit"])
            if "amp" in kwargs:
                self.set_amplitude(channel, kwargs["amp"])
            if "offset" in kwargs:
                self.set_offset(channel, kwargs["offset"])
        if "high" in kwargs or "low" in kwargs:
            if "high" in kwargs:
                self.set_high(channel, kwargs["high"])
            if "low" in kwargs:
                self.set_low(channel, kwargs["low"])
        if "phase" in kwargs:
            self.set_phase(channel, kwargs["phase"])

        if wave in ("SQU", "SQUARE", "PULSE") and "duty" in kwargs:
            self.set_duty(channel, kwargs["duty"])
        if wave == "RAMP" and "symmetry" in kwargs:
            self.set_symmetry(channel, kwargs["symmetry"])
        if wave == "PULSE":
            if "rise_time" in kwargs:
                self.set_rise_time(channel, kwargs["rise_time"])
            if "fall_time" in kwargs:
                self.set_fall_time(channel, kwargs["fall_time"])

    # --- Preset methods ---

    def configure_sine(self, channel: int, **kwargs):
        """
        Method for square waveform configuration.
        Available parameters in **kwargs:
        \t
        - freq (Hz),
        - amp_unit ('Vpp' or 'Vrms') and amp (V) and offset (V) or
        - high (V) and low (V),
        - phase (deg).

        :param channel: Channel No. Value 1, 2.
        :param kwargs: Dict with parameters.
        :return: None
        """
        self.configure_waveform(channel, waveform="SINE", **kwargs)

    def configure_square(self, channel: int, **kwargs) -> None:
        """
        Method for square waveform configuration.
        Available parameters in **kwargs:
        \t
        - freq (Hz),
        - amp_unit ('Vpp' or 'Vrms') and amp (V) and offset (V) or
        - high (V) and low (V),
        - phase (deg),
        - duty (%).

        :param channel: Channel No. Value 1, 2.
        :param kwargs: Dict with parameters.
        :return: None
        """
        self.configure_waveform(channel, waveform="SQUARE", **kwargs)

    def configure_ramp(self, channel: int, **kwargs):
        """
        Method for ramp waveform configuration.
        \n
        Available parameters in **kwargs:
        \t
        - freq (Hz),
        - amp_unit ('Vpp' or 'Vrms') and amp (V) and offset (V) or
        - high (V) and low (V),
        - phase (deg),
        - symmetry (%).

        :param channel: Channel No. Value 1, 2.
        :param kwargs: Dict with parameters.
        :return: None
        """
        self.configure_waveform(channel, waveform="RAMP", **kwargs)

    def configure_pulse(self, channel: int, **kwargs):
        """
        Method for pulse waveform configuration.
        \n
        Available parameters in **kwargs:
        \t
        - freq (Hz),
        - amp_unit ('Vpp' or 'Vrms') and amp (V) and offset (V) or
        - high (V) and low (V),
        - phase (deg),
        - duty (%),
        - rise_time (s),
        - fall time (s).

        :param channel: Channel No. Value 1, 2.
        :param kwargs: Dict with parameters.
        :return: None
        """
        self.configure_waveform(channel, waveform="PULSE", **kwargs)

    def configure_arb(self, channel: int, **kwargs):
        """
        Method for arb waveform configuration.
        \n
        Available parameters in **kwargs:
        \t
        - wave_source (Internal or External),
        - wave_file,
        - freq (Hz) or period (s),
        - amp_unit ('Vpp' or 'Vrms'), amp (V) and offset (V) or
        - high (V) and low (V),
        - phase (deg).

        :param channel: Channel No. Value 1, 2.
        :param kwargs: Dict with parameters.
        :return: None
        """
        self.configure_waveform(channel, waveform="ARB", **kwargs)


    def configure_dc(self, channel: int, **kwargs):
        """
        Method for dc waveform configuration.
        \n
        Available parameters in **kwargs:
        \t
        - dc (V).

        :param channel: Channel No. Value 1, 2.
        :param kwargs: Dict with parameters.
        :return: None
        """
        self.configure_waveform(channel, waveform="DC", **kwargs)

# --- Usage example ---

if __name__ == "__main__":
    ch1, ch2 = 1, 2

    # Set device address
    device_address = 'USB0::0x6656::0x0834::AWG1524090001::INSTR'
    gen = UTG900E(device_address)
    gen.reset()
    print("IDN:", gen.identify())
    gen.configure_pulse(
        channel=2,
        freq=2000,
        # period=10.01,
        # amp=5,
        # amp_unit="Vrms",
        # offset=0,
        high=10,
        low=-1,
        phase=-28.3,
        duty=50.5,
        rise_time=0.000000150,
        fall_time=0.000000150,
    )
    print("Inversion: ", gen.get_inversion(ch1))
    # print("Inversion: ", gen.get_inversion(3))
    print("Output: ", gen.get_output(ch1))
    gen.set_output(2, True)
    input("Press Enter for signal disable...")
    gen.set_output(2, False)
    gen.close()
