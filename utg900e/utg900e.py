import pyvisa
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UTG900E:
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
            gen.set_output(1) Set the channel 1 output ON
            gen.set_output(1, False) Set the channel 1 output OFF
        """
        if channel in (0, 1):
            self.write(f":CHANnel{channel}:OUTPut {'ON' if state else 'OFF'}")
        else:
            raise


    def get_output(self, channel: int) -> int:
        """
         Function
            Returns the specified channel output status, 0 in OFF, 1 in ON
         Example
            gen.set_output(1)
            gen.get_output(1) Returns 1, because channel 1 output is enabled
        """
        if channel in (0, 1):
            return self.query(f":CHANnel{channel}:OUTPut?")
        else:
            raise


    def set_inversion(self, channel: int, inversion=False):
        """
         Function
            Set the specified channel reverse ON (True) / OFF (False).
         Example
            gen.set_inversion(1, True) Set the reverse output of channel 1 ON
        """
        if channel in (0, 1):
            self.write(f":CHANnel{channel}:INVersion {"ON" if inversion else "OFF"}")
        else:
            raise


    def get_inversion(self, channel: int):
        """
         Function
            Returns the specified channel reverse, 0 in OFF, 1 in ON.
         Example
            gen.set_inversion(1, True)
            gen.get_inversion(1) Returns 1, because channel 1 is reversed
        """
        if channel in (0, 1):
            return self.query(f":CHANnel{channel}:INVersion?")
        else:
            raise


    def set_sync(self, channel: int, sync=False):
        """
         Function
            Set the sync output of channel.
            Note: Only one sync output interface in the device,
            and can only open the sync output of one channel.
         Example
            gen.set_sync(1, True) Set the sync output of channel 1 ON
        """
        if channel in (0, 1):
            self.write(f":CHANnel{channel}:OUTPut:SYNC {"ON" if sync else "OFF"}")
        else:
            raise


    def get_sync(self, channel: int):
        """
         Function
            Returns the sync output of specified channel, 0 in OFF, 1 in ON
         Example
            gen.set_sync(1, True)
            gen.get_sync(1) Returns 1, because channel 1 is synced
        """
        if channel in (0, 1):
            return self.query(f":CHANnel{channel}:OUTPut:SYNC?")
        else:
            raise


    def limit_enable(self, channel: int, enable=True):
        pass


    def set_waveform(self, channel, waveform):
        self.write(f":CHANnel{channel}:BASE:WAVe {waveform.upper()}")


    def set_mode(self, channel, mode):
        self.write(f":CHANnel{channel}:MODe {mode.upper()}")

    def set_frequency(self, channel, freq_hz):
        self.write(f":CHANnel{channel}:BASE:FREQuency {freq_hz}")

    def set_amplitude(self, channel, amplitude_v):
        self.write(f":CHANnel{channel}:BASE:AMPLitude {amplitude_v}")

    def set_offset(self, channel, offset_v):
        self.write(f":CHANnel{channel}:BASE:OFFSet {offset_v}")

    def set_phase(self, channel, phase_deg):
        self.write(f":CHANnel{channel}:BASE:PHAse {phase_deg}")

    def set_duty(self, channel, duty_percent):
        if not (0 <= duty_percent <= 100):
            raise ValueError("Duty must be 0–100%")
        self.write(f":CHANnel{channel}:BASE:DUTY {duty_percent}")

    def set_symmetry(self, channel, symmetry_percent):
        if not (0 <= symmetry_percent <= 100):
            raise ValueError("Symmetry must be 0–100%")
        self.write(f":CHANnel{channel}:RAMP:SYMMetry {symmetry_percent}")

    def set_rise_time(self, channel, rise_s):
        self.write(f":CHANnel{channel}:PULSe:RISe {rise_s}")

    def set_fall_time(self, channel, fall_s):
        self.write(f":CHANnel{channel}:PULSe:FALL {fall_s}")

    # --- Universal signal setting methods ---

    def configure_waveform(self, channel=1, waveform="SINE", mode="CONTinue", **kwargs):
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
            self.set_frequency(channel, kwargs["period"])
        elif "freq" in kwargs and "period" in kwargs:
            raise

        if "amp" in kwargs:
            self.set_amplitude(channel, kwargs["amp"])
        if "offset" in kwargs:
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

    # --- Presett methods ---

    def configure_sine(self, channel=1, **kwargs):
        self.configure_waveform(channel, waveform="SINE", **kwargs)

    def configure_square(self, channel=1, **kwargs):
        self.configure_waveform(channel, waveform="SQUARE", **kwargs)

    def configure_ramp(self, channel=1, **kwargs):
        self.configure_waveform(channel, waveform="RAMP", **kwargs)

    def configure_pulse(self, channel=1, **kwargs):
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
