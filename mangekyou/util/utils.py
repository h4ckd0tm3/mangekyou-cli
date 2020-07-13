from typing import *
from mangekyou.beans.profile import Profile


def convert_to_profile(profiles: List[List]) -> List:
    ret = list()
    for profile in profiles:
        ret.append(Profile(profile["url"], profile["picture"], profile["association"]))

    return ret
