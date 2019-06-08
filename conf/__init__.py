import configparser
import os

__all__ = ["status"]

cfg = configparser.ConfigParser()
cfg.read(os.path.join('Config', 'Config.ini'))

status = {
    "SUCCESS": cfg.get("status", "SUCCESS"),
    "FAIL": cfg.get("status", "SUCCESS"),
    "ERROR": cfg.get("status", "ERROR")
}