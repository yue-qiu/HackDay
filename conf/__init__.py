import configparser
import os

__all__ = ["status"]

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding="utf8")

status = {
    "SUCCESS": cfg.get("status", "SUCCESS"),
    "FAIL": cfg.get("status", "FAIL"),
    "ERROR": cfg.get("status", "ERROR"),
    "PERMISSION": cfg.get("status", "PERMISSION"),
    "UNACTIVE": cfg.get("status", "UNACTIVE"),
}
