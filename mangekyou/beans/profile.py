from typing import *
from mangekyou.beans.target import Target


class Profile:
    url: str
    picture: str
    info: Dict
    association: float

    def __init__(self, url: str, picture: str, association: float):
        self.url = url
        self.picture = picture
        self.association = association

    def set_picture(self, picture: str):
        self.picture = picture

    def set_info(self, info: Dict):
        self.info = info

    def toDict(self):
        ret = dict()
        ret["url"] = self.url
        ret["picture"] = self.picture
        ret["association"] = self.association

        return ret
