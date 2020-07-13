import sys
import json
import inspect
import colorlog

from typing import *
from pathlib import Path
from logging import Logger
from mangekyou.beans.credentials import Credentials
from mangekyou.beans.facematchconfig import FaceMatchConfig


class ConfigUpdate:
    def __init__(self, config: 'Config'):
        self.success = True
        self.log_level = colorlog.root.getEffectiveLevel()
        self.temp_folder = config.temp_folder
        self.plugins_folder = config.plugins_folder
        self.categories_filter = config.categories_filter
        self.credentials = config.credentials
        self.facematchconfig = config.facematchconfig

    def fail(self):
        self.success = False

    success: bool
    log_level: Union[str, int]

    temp_folder: str
    plugins_folder: str
    credentials: Credentials
    facematchconfig: FaceMatchConfig

    categories_filter: Dict[str, object]


class Config:
    logger: Logger
    handler: colorlog.StreamHandler
    config_path: str

    temp_folder: str
    plugins_folder: str
    credentials: Credentials
    facematchconfig: FaceMatchConfig

    categories_filter: Dict[str, object]
    log_level: Union[str, int]

    def __init__(self, config_path: str, handler: colorlog.StreamHandler):
        self.temp_folder = ""
        self.plugins_folder = ""
        self.credentials = Credentials()
        self.facematchconfig = FaceMatchConfig()

        self.categories_filter = dict()

        self.handler = handler
        self.logger = colorlog.getLogger("mangekyou:config")
        self.logger.addHandler(self.handler)

        self.config_path = config_path

        self.logger.info(f"Using config: '{self.config_path}'")
        if not self.load():
            raise Exception("Could not load initial configuration from '{self.config_path}'")

    def _parse_log_level(self, upd: ConfigUpdate, log_level: object):
        if not isinstance(log_level, str) and not isinstance(log_level, int):
            self.logger.error(f"log_level: must be int or str, {type(log_level)} given")
            return upd.fail()

        log_level = cast(Union[int, str], log_level)

        LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
        if isinstance(log_level, str) and log_level not in LOG_LEVELS:
            self.logger.error(f"log_level: string must be one of {LOG_LEVELS}, '{log_level}' given")
            return upd.fail()

        upd.log_level = log_level

    def _parse_temp_folder(self, upd: ConfigUpdate, temp_folder: object):
        if not isinstance(temp_folder, str):
            self.logger.error(f"temp_folder: must be int or str, {type(temp_folder)} given")
            return upd.fail()

        if temp_folder == "DEFAULT":
            temp = Path.home() / ".mangekyou" / "temp"
            upd.temp_folder = str(temp)
        else:
            upd.temp_folder = temp_folder

    def _parse_plugin_folder(self, upd: ConfigUpdate, plugins_folder: object):
        if not isinstance(plugins_folder, str):
            self.logger.error(f"plugins: must be int or str, {type(plugins_folder)} given")
            return upd.fail()

        if plugins_folder == "DEFAULT":
            plugins = Path.home() / ".mangekyou" / "plugins"
            upd.plugins_folder = str(plugins)
        else:
            upd.plugins_folder = plugins_folder

        if self.plugins_folder in sys.path:
            sys.path.remove(self.plugins_folder)

        sys.path.append(upd.plugins_folder)

    def _parse_credentials(self, upd: ConfigUpdate, credentials: object):
        if not isinstance(credentials, dict):
            self.logger.error(f"credentials: must be dict, {type(credentials)} given")
            return upd.fail()

        if "username" in credentials and "password" in credentials:
            if not isinstance(credentials["username"], str):
                self.logger.error(f"username: must be str, {type(credentials['username'])} given")
                return upd.fail()
            else:
                upd.credentials.set_username(credentials["username"])

            if not isinstance(credentials["password"], str):
                self.logger.error(f"password: must be str, {type(credentials['password'])} given")
                return upd.fail()
            else:
                upd.credentials.set_password(credentials["password"])
        else:
            self.logger.error("credentials: must contain username and password field.")
            return upd.fail()

    def _parse_face_recognition_options(self, upd: ConfigUpdate, facematch: object):
        if not isinstance(facematch, dict):
            self.logger.error(f"facematch: must be dict, {type(facematch)} given")
            return upd.fail()

        if "location_model" in facematch and "tolerance" in facematch and "encoding_model" in facematch and "encoding_jitter" in facematch:
            if not isinstance(facematch["location_model"], str):
                self.logger.error(f"location_model: must be str, {type(facematch['location_model'])} given")
                return upd.fail()
            else:
                upd.facematchconfig.set_location_model(facematch["location_model"])

            if not isinstance(facematch["tolerance"], float):
                self.logger.error(f"tolerance: must be float, {type(facematch['location_model'])} given")
                return upd.fail()
            else:
                upd.facematchconfig.set_tolerance(facematch["tolerance"])

            if not isinstance(facematch["encoding_model"], str):
                self.logger.error(f"encoding_model: must be str, {type(facematch['encoding_model'])} given")
                return upd.fail()
            else:
                upd.facematchconfig.set_encoding_model(facematch["encoding_model"])

            if not isinstance(facematch["encoding_jitter"], int):
                self.logger.error(f"encoding_jitter: must be int, {type(facematch['encoding_jitter'])} given")
                return upd.fail()
            else:
                upd.facematchconfig.set_encoding_jitter(facematch["encoding_jitter"])
        else:
            self.logger.error("facematch: one or more required fields are missing.")
            return upd.fail()

    def _creat_plugin_categories_filter(self, upd: ConfigUpdate):
        import categories

        categories_filter = dict()
        for c in inspect.getmembers(categories, inspect.isclass):
            if c[1].__module__.endswith("categories"):
                categories_filter[c[0]] = c[1]

        upd.categories_filter = categories_filter

    def _apply(self, upd: ConfigUpdate):
        colorlog.root.setLevel(upd.log_level)

        self.temp_folder = upd.temp_folder
        self.plugins_folder = upd.plugins_folder
        self.categories_filter = upd.categories_filter
        self.credentials = upd.credentials
        self.facematchconfig = upd.facematchconfig

    def load(self) -> bool:
        upd = ConfigUpdate(self)

        try:
            with open(self.config_path, "r") as f:
                j = json.load(f)

            if "log_level" in j:
                self._parse_log_level(upd, j["log_level"])

            if "temp_folder" in j:
                self._parse_temp_folder(upd, j["temp_folder"])

            if "plugins_folder" in j:
                self._parse_plugin_folder(upd, j["plugins_folder"])

            if "facematch" in j:
                self._parse_face_recognition_options(upd, j["facematch"])

            if "credentials" in j:
                self._parse_credentials(upd, j["credentials"])

            self._creat_plugin_categories_filter(upd)

        except FileNotFoundError:
            self.logger.error("configuration file does not exist")
            upd.fail()
        except json.JSONDecodeError:
            self.logger.error("invalid JSON in configuration file")
            upd.fail()

        if upd.success:
            self._apply(upd)
        return upd.success
