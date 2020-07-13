from typing import *
from pathlib import Path

import os
import json
import datetime


def userinput():
    data = dict()
    name = input("[*] Name (required): ")
    face = input("[*] Picture-Path (required): ")

    profiles = list()
    instagram = dict()
    ig_url = ""
    #fb_url = ""
    #tw_url = ""

    ig_check = False
    ki = input("[?] Known Instagram Profile? [y/N]")
    if ki.upper() == "Y":
        ig_check = True

    if ig_check:
        ig_url = input("[*] Instagram Profile URL: ")

    """
    fb_check = False
    kf = input("[?] Known Facebook Profile? [y/N]")
    if kf.upper() == "Y":
        fb_check = True

    if fb_check:
        fb_url = input("[*] Facebook Profile URL: ")

    tw_check = False
    kt = input("[?] Known Twitter Profile? [y/N]")
    if kt.upper() == "Y":
        tw_check = True

    if tw_check:
        tw_url = input("[*] Twitter Profile URL: ")
    """

    data["name"] = name
    data["pictures"] = face
    instagram["url"] = ig_url
    instagram["picture"] = ""
    instagram["association"] = 1.0
    profiles.append(instagram)
    #profiles["facebook"] = fb_url
    #profiles["twitter"] = tw_url
    data["profiles"] = profiles

    return data


def create_target(targets_folder, data):
    now = datetime.datetime.now()

    target_folder = targets_folder / f"{now.strftime('%Y%m%d')}_{data['name'].replace(' ', '_')}"
    target_folder.mkdir(exist_ok=True)

    target_pictures = target_folder / "pictures"
    target_pictures.mkdir(exist_ok=True)

    target_json_file = target_folder / "target.json"

    face = data["pictures"]
    data["pictures"] = str(target_pictures)

    os.system(f"cp {face} {str(target_pictures)}/face.{face.split('.')[1]}")

    data["face_encodings"] = str(target_folder / "face.encodings")

    with open(str(target_json_file), "w+") as f:
        json.dump(data, f)


def main():
    print("[~] Starting mangekyou target generator...")
    dotfolder = Path.home() / ".mangekyou"
    targets = dotfolder / "targets"
    targets.mkdir(parents=True, exist_ok=True)

    data = userinput()
    create_target(targets, data)


if __name__ == "__main__":
    main()
