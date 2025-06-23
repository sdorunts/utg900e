import pyvisa
import logging

# Логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UTG900E:
    def __init__(self, device_addr=None):
        self.rm = pyvisa.ResourceManager()
        self.inst = None
        if device_addr:
            self.connect(device_addr)
        else:
            logger.warning("Устройство не подключено: не указан адрес.")

    def connect(self, device_addr):
        try:
            self.inst = self.rm.open_resource(device_addr)
            self.inst.write_termination = '\n'
            self.inst.read_termination = '\n'
            logger.info(f"Подключено к {device_addr}")
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            raise

    def close(self):
        if self.inst:
            self.inst.close()
            logger.info("Соединение закрыто.")

    def write(self, command):
        logger.debug(f"→ {command}")
        self.inst.write(command)

    def query(self, command):
        logger.debug(f"→ {command}")
        return self.inst.query(command)

    def identify(self):
        return self.query("*IDN?")

    # --- Low-level commands (SCPI wrappers) ---

    def set_output(self, channel, state=True):
        self.write(f":CHANnel{channel}:OUTPut {'ON' if state else 'OFF'}")

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

    