import os

from typing import *
from glob import glob
from pathlib import Path
from mangekyou.util import utils
from mangekyou.core.pluginloader import *
from mangekyou.beans.target import Target
from mangekyou.beans.profile import Profile
from mangekyou.core.facematch import Facematch
from mangekyou.core.reporting import Reporting


class Mangekyou:
    logger: Logger
    config: Config
    target: Target
    target_path: str
    facematch: Facematch
    reporting: Reporting

    def __init__(self, config: Config, target_path: str):
        self.config = config
        self.logger = colorlog.getLogger("mangekyou")
        self.logger.addHandler(self.config.handler)

        self.target_path = target_path
        self.target = Target(target_path, self.logger)
        self.logger.debug(f"Set target to '{target_path}'")

        self.facematch = Facematch(self.config)
        self.reporting = Reporting(self.config)

    def run(self):
        self.logger.debug("Loading Target Picture Paths")

        if len(self.target.face_encodings) == 0:
            images = glob(f"{self.target.pictures}/*")
            known_images = self.facematch.load_images(images)

            for image in known_images:
                locations = self.facematch.get_face_locations(image)
                encoding = self.facematch.get_face_encodings(image, locations)[0]
                self.target.add_face_encoding(encoding)

        self.logger.info("Loading Plugins")
        pl = PluginLoader(self.config)
        plugins = pl.load_plugins()

        finders = list()
        crawlers = list()

        for plugin in plugins:
            if plugin.category == "Finder":
                finders.append(plugin)
            elif plugin.category == "Crawler":
                crawlers.append(plugin)

        for finder in finders:
            plugin_logger = colorlog.getLogger(f"mangekyou:plugin:{finder.name.replace(' ', '')}")
            plugin_logger.addHandler(self.config.handler)

            finder.plugin_object.setLogger(plugin_logger)
            finder.plugin_object.setConfigParams(self.config.temp_folder)
            finder.plugin_object.setCredentials(self.config.credentials.username, self.config.credentials.password)

            finder.plugin_object.doLogin()
            profiles = utils.convert_to_profile(finder.plugin_object.getProfiles(self.target.name))

            matches = self.facematch.compare(self.target.face_encodings, profiles)

            for match in matches:
                profile = match[0]
                profile_pictrue_path = Path(profile.picture)
                store_path = Path(self.target.pictures) / profile_pictrue_path.name

                os.system(f"mv {str(profile_pictrue_path)} {str(store_path)}")
                profile.set_picture(str(store_path))

                self.target.add_profile(profile)
                self.target.add_face_encoding(match[1])

            finder.plugin_object.kill()

        for crawler in crawlers:
            plugin_logger = colorlog.getLogger(f"mangekyou:plugin:{crawler.name.replace(' ', '')}")
            plugin_logger.addHandler(self.config.handler)

            crawler.plugin_object.setLogger(plugin_logger)
            crawler.plugin_object.setCredentials(self.config.credentials.username, self.config.credentials.password)

            crawler.plugin_object.doLogin()

            for profile in self.target.profiles:
                info = crawler.plugin_object.getInfo(profile.url)
                if info:
                    profile.set_info(info)

        self.target.save(self.target_path)
        self.reporting.target_to_pdf(self.target, self.target_path)
