import json
import pickle

from typing import *
from glob import glob
from pathlib import Path
from logging import Logger
from mangekyou.util import utils

class Target:
    name: str
    face: str
    pictures: str
    profiles: List
    face_encodings_path: str
    face_encodings: List

    logger: Logger

    def __init__(self, path: str, logger: Logger):
        self._parse_target(f"{path}/target.json")
        self.logger = logger

    def _parse_target(self, path):
        with open(path, "r") as f:
            js = json.loads(f.read())

            if "name" in js and "pictures" in js and "profiles" in js and "face_encodings" in js:
                if isinstance(js["name"], str):
                    self.name = js["name"]
                else:
                    self.logger.error(f"name: must be str, {type(js['name'])} given")

                if isinstance(js["pictures"], str):
                    self.pictures = js["pictures"]
                    self.face = glob(f"{self.pictures}/face.*")[0]
                else:
                    self.logger.error(f"pictures: must be str, {type(js['pictures'])} given")

                if isinstance(js["profiles"], List):
                    self.profiles = utils.convert_to_profile(js["profiles"])
                else:
                    self.logger.error(f"profiles: must be List, {type(js['profiles'])} given")

                if isinstance(js["face_encodings"], str):
                    self.face_encodings_path = js["face_encodings"]
                    self.face_encodings = self._load_face_encoding()
                else:
                    self.logger.error(f"face_encodings: must be str, {type(js['face_encodings'])} given")

            else:
                self.logger.error("Target format error. Your target.json has the wrong format.")

    def _load_face_encoding(self) -> List:
        face_encodings_pickle = Path(self.face_encodings_path)

        if face_encodings_pickle.exists():
            with face_encodings_pickle.open("rb") as f:
                face_encodings = pickle.load(f)

            return face_encodings
        else:
            return list()

    def add_face_encoding(self, encoding):
        self.face_encodings.append(encoding)

    def add_profile(self, profile):
        self.profiles.append(profile)

    def save(self, path: str):
        target = dict()
        target["name"] = self.name
        target["pictures"] = self.pictures

        profiles = list()
        for profile in self.profiles:
            profiles.append(profile.toDict())

        target["profiles"] = profiles
        target["face_encodings"] = self.face_encodings_path

        with open(f"{path}/target.json", "w") as f:
            json.dump(target, f)

        with open(self.face_encodings_path, "wb") as f:
            pickle.dump(self.face_encodings, f)