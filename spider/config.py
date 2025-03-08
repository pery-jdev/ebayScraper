
from pathlib import Path
class Config(object):
    BASE_DIR = Path(__file__).resolve().parent.parent
    TEMP_DIR = BASE_DIR / 'temp'
    DEBUG: bool = True

    # setting for selenium
    DRIVER_PATH = TEMP_DIR / 'driver'