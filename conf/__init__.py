import configparser
import os

__all__ = ["status"]

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding="utf8")

status = {
    "SUCCESS": cfg.get("status", "SUCCESS"),
    "FAIL": cfg.get("status", "SUCCESS"),
    "ERROR": cfg.get("status", "ERROR")
}