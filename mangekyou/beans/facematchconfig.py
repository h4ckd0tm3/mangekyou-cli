from typing import *


class FaceMatchConfig:
    location_model: str
    encoding_model: str
    encoding_jitter: int
    tolerance: float

    def __init__(self):
        pass

    def set_location_model(self, model: str):
        self.location_model = model

    def set_encoding_model(self, model: str):
        self.encoding_model = model

    def set_encoding_jitter(self, jitter: int):
        self.encoding_jitter = jitter

    def set_tolerance(self, tolerance: float):
        self.tolerance = tolerance
