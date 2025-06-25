import pyvisa
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UTG900E:
    channel_numbers = (0, 1)
    available_amplitude_units = ("VPP", "VRMS")

    def __init__(self, device_addr=None):
        self.rm = pyvisa.ResourceManager()
        self.inst = None
        if device_addr:
            self.connect(device_addr)
        else:
            logger.warning("Device has not been connected: address hasn't been priveded.")

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
            gen.set_output(1) Set the channel 1 output ON \n
            gen.set_output(1, False) Set the channel 1 output OFF
        """
        if channel not in self.channel_numbers:
            raise
        self.write(f":CHANnel{channel}:OUTPut {'ON' if state else 'OFF'}")


    def get_output(self, channel: int) -> int:
        """
         Function
            Returns the specified channel output status, 0 in OFF, 1 in ON
         Example
            gen.set_output(1) \n
            gen.get_output(1) Returns 1, because channel 1 output is enabled
        """
        if channel not in self.channel_numbers:
            raise
        return self.query(f":CHANnel{channel}:OUTPut?")


    def set_inversion(self, channel: int, inversion=False):
        """
         Function
            Set the specified channel reverse ON (True) / OFF (False).
         Example
            gen.set_inversion(1, True) Set the reverse output of channel 1 ON
        """
        if channel not in self.channel_numbers:
            raise
        self.write(f":CHANnel{channel}:INVersion {"ON" if inversion else "OFF"}")


    def get_inversion(self, channel: int):
        """
         Function
            Returns the specified channel reverse, 0 in OFF, 1 in ON.
         Example
            gen.set_inversion(1, True) \n
            gen.get_inversion(1) Returns 1, because channel 1 is reversed
        """
        if channel not in self.channel_numbers:
            raise
        return self.query(f":CHANnel{channel}:INVersion?")


    def set_sync(self, channel: int, sync=False):
        """
         Function
            Set the sync output of channel.
            Note: Only one sync output interface in the device,
            and can only open the sync output of one channel.
         Example
            gen.set_sync(1, True) Set the sync output of channel 1 ON
        """
        if channel not in self.channel_numbers:
            raise
        self.write(f":CHANnel{channel}:OUTPut:SYNC {"ON" if sync else "OFF"}")


    def get_sync(self, channel: int):
        """
         Function
            Returns the sync output of specified channel, 0 in OFF, 1 in ON
         Example
            gen.set_sync(1, True) \n
            gen.get_sync(1) Returns 1, because channel 1 is synced
        """
        if channel not in self.channel_numbers:
            raise
        return self.query(f":CHANnel{channel}:OUTPut:SYNC?")


    def limit_enable(self, channel: int, enable=True):
        """
         Function
            Set the amplitude limiting ON/OFF of specified channel
         Example
            gen.limit_enable(1) Set the amplitude limiting of channel 1 ON
        """
        if channel not in self.channel_numbers:
            raise
        self.write(f":CHANnel{channel}:LIMit:ENABle {"ON" if enable else "OFF"}")


    def is_limit_enable(self, channel: int) -> int:
        """
         Function
            Returns the amplitude limiting status of specified channel
         Example
            gen.limit_enable(1) \n
            gen.is_limit_enable(1) Returns 1, because channel 1 limit is enable
        """
        if channel not in self.channel_numbers:
            raise
        return self.query(f":CHANnel{channel}:LIMit:ENABle?")


    def set_lower_limit(self, channel: int, limit_v: float):
        """
         Function
            Set the lower amplitude limit of specified channel.
            <voltage> means the voltage, and its unit is the
            specified unit of current channel
         Example
            get.set_lower_limit(1, 2) Set the lower amplitude limit of channel 1 to 2V
        """
        if channel not in self.channel_numbers:
            raise
        self.write(f":CHANnel{channel}:LIMit:LOWer {limit_v}")


    def get_lower_limit(self, channel: int) -> float:
        """
         Function
            Returns the lower amplitude limit of specified channel, using scientific notation to return.
         Example
            get.get_lower_limit(1) Returns 2e+0
        """
        if channel not in self.channel_numbers:
            raise
        return self.query(f":CHANnel{channel}:LIMit:LOWer?")


    def set_upper_limit(self, channel: int, limit_v: float):
        """
         Function
            Set the upper amplitude limit of specified channel.
            <voltage> means voltage, and its unit is the specified unit of current channel.
         Example
            get.set_upper_limit(1, 2) Set the upper amplitude limit of channel 1 to 2V
        """
        if channel not in self.channel_numbers:
            raise
        self.write(f":CHANnel{channel}:LIMit:UPPer {limit_v}")


    def get_upper_limit(self, channel: int) -> float:
        """
         Function
            Returns the upper amplitude limit of specified channel, using scientific notation to return.
         Example
            get.get_upper_limit(1) Returns 2e+0
        """
        if channel not in self.channel_numbers:
            raise
        return self.query(f":CHANnel{channel}:LIMit:UPPer?")


    def set_amplitude_unit(self, channel: int, unit="VPP"):
        """
         Function
            Set the unit of output amplitude in specified channel
            Available units are VPP and VRMS
         Example
            gen.set_amplitude_unit(1, "Vrms") Set the unit of output amplitude in channel 1 to VRMS
        """
        if channel not in self.channel_numbers:
            raise
        unit = unit.upper()
        if unit not in self.available_amplitude_units:
            raise
        self.write(f":CHANnel{channel}:AMPLitude:UNIT {unit}")


    def get_amplitude_unit(self, channel: int) -> str:
        """
         Function
            Returns the unit of output amplitude in specified channel.
         Example
            gen.set_amplitude_unit(1, "Vrms") Set the unit of output amplitude in channel 1 to VRMS
        """
        pass


    def set_load(self, channel: int, resistance_r=50):
        pass


    def get_load(self, channel: int) -> int:
        pass


    def set_waveform(self, channel: int, waveform: str):
        self.write(f":CHANnel{channel}:BASE:WAVe {waveform.upper()}")


    def get_waveform(self, channel: int) -> str:
        pass


    def set_frequency(self, channel: int, freq_hz: float):
        self.write(f":CHANnel{channel}:BASE:FREQuency {freq_hz}")


    def get_frequency(self, channel: int):
        pass


    def set_period(self, channel: int, period_s: float):
        pass


    def get_period(self, channel: int) -> float:
        pass


    def set_phase(self, channel, phase_deg):
        self.write(f":CHANnel{channel}:BASE:PHAse {phase_deg}")


    def get_phase(self, channel: int) -> float:
        pass


    def set_amplitude(self, channel: int, amplitude_v: float):
        if channel not in self.channel_numbers:
            raise

        if self.is_limit_enable(channel):
            lower_limit = float(self.get_lower_limit(channel))
            upper_limit = float(self.get_upper_limit(channel))
            # upper_limit = self.get_upper_limit(channel)

        self.write(f":CHANnel{channel}:BASE:AMPLitude {amplitude_v}")


    def get_amplitude(self, channel: int):
        pass


    def set_offset(self, channel: int, offset_v: float):
        self.write(f":CHANnel{channel}:BASE:OFFSet {offset_v}")


    def get_offset(self, channel: int) -> float:
        pass


    def set_high(self, channel: int, high_v: float):
        pass


    def get_high(self, channel: int) -> float:
        pass


    def set_low(self, channel: int, low_v: float):
        pass


    def get_low(self, channel: int) -> float:
        pass


    def set_duty(self, channel: int, duty_percent: float):
        if not (0 <= duty_percent <= 100):
            raise ValueError("Duty must be 0–100%")
        self.write(f":CHANnel{channel}:BASE:DUTY {duty_percent}")


    def get_duty(self, channel: int) -> float:
        pass


    def set_symmetry(self, channel: int, symmetry_percent: float):
        if not (0 <= symmetry_percent <= 100):
            raise ValueError("Symmetry must be 0–100%")
        self.write(f":CHANnel{channel}:RAMP:SYMMetry {symmetry_percent}")


    def get_symmetry(self, channel: int) -> float:
        pass


    def set_rise_time(self, channel: int, rise_s: float):
        self.write(f":CHANnel{channel}:PULSe:RISe {rise_s}")


    def get_rise_time(self, channel: int) -> float:
        pass


    def set_fall_time(self, channel: int, fall_s: float):
        self.write(f":CHANnel{channel}:PULSe:FALL {fall_s}")


    def get_fall_time(self, channel: int) -> float:
        pass


    def set_mode(self, channel: int, mode: str):
        self.write(f":CHANnel{channel}:MODe {mode.upper()}")
        
        
    def get_mode(self, channel: int) -> str:
        pass
    
    



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
        self.set_mode(channel, mode)
        self.set_waveform(channel, waveform)

        if "freq" in kwargs and "period" not in kwargs:
            self.set_frequency(channel, kwargs["freq"])
        elif "freq" not in kwargs and "period" in kwargs:
            self.set_period(channel, kwargs["period"])
        elif "freq" in kwargs and "period" in kwargs:
            raise

        if "amp_unit" in kwargs and ("high", "low") not in kwargs:
            self.set_amplitude_unit(channel, kwargs["amp_unit"])
        if "amp" in kwargs and ("high", "low") not in kwargs:
            self.set_amplitude(channel, kwargs["amp"])
        if "offset" in kwargs and ("high", "low") not in kwargs:
            self.set_offset(channel, kwargs["offset"])


        if "phase" in kwargs:
            self.set_phase(channel, kwargs["phase"])

        wave = waveform.upper()
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
        self.configure_waveform(channel, waveform="SINE", **kwargs)

    def configure_square(self, channel: int, **kwargs):
        self.configure_waveform(channel, waveform="SQUARE", **kwargs)

    def configure_ramp(self, channel: int, **kwargs):
        self.configure_waveform(channel, waveform="RAMP", **kwargs)

    def configure_pulse(self, channel: int, **kwargs):
        self.configure_waveform(channel, waveform="PULSE", **kwargs)

# --- Usage example ---

if __name__ == "__main__":
    ch1, ch2 = 1, 2

    # Set device address
    device_address = 'USB0::0x6656::0x0834::AWG1524090001::INSTR'
    gen = UTG900E(device_address)
    gen.reset()
    print("IDN:", gen.identify())
    gen.configure_square(
        channel=1,
        freq=1000.001000,
        amp=2,
        offset=0.45,
        phase=-18.3,
        duty=55.5
    )
    print("Inversion: ", gen.get_inversion(ch1))
    gen.set_output(1, True)
    input("Press Enter for signal disable...")
    gen.set_output(1, False)
    gen.close()
