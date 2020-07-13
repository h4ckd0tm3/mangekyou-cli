import numpy as np
import face_recognition

from typing import *
from mangekyou.core.config import Config
from mangekyou.beans.profile import Profile


class Facematch():
    config: Config

    def __init__(self, config: Config):
        self.config = config

    def load(self, image: str):
        return face_recognition.load_image_file(image)

    def load_images(self, toload: List) -> List:
        loaded = list()
        for element in toload:
            if isinstance(element, Profile):
                loaded.append(self.load(element.picture))
            else:
                loaded.append(self.load(element))

        return loaded

    def get_face_locations(self, image) -> List:
        return face_recognition.face_locations(image, model=self.config.facematchconfig.location_model)

    def get_face_encodings(self, image, face_locations: List) -> List:
        return face_recognition.face_encodings(image, face_locations, self.config.facematchconfig.encoding_jitter,
                                               self.config.facematchconfig.encoding_model)

    def get_face_distances(self, known_encodings, face_encoding):
        return face_recognition.face_distance(known_encodings, face_encoding)

    def compare(self, known_encodings, unknown: List[Profile]) -> List[Tuple[Profile, List]]:
        matched_profiles = list()

        unknown_images = self.load_images(unknown)

        for image, profile in zip(unknown_images, unknown):
            locations = self.get_face_locations(image)
            encodings = self.get_face_encodings(image, locations)

            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(known_encodings, face_encoding,
                                                         self.config.facematchconfig.tolerance)

                if True in results:
                    matched_profiles.append((profile, face_encoding))

        return matched_profiles
