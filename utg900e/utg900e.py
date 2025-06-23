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
