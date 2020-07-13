from yapsy.PluginManager import PluginManager
from mangekyou.core.config import Config
from logging import Logger

import colorlog


class PluginLoader:
    logger: Logger
    config: Config
    manager: PluginManager

    def __init__(self, config: Config):
        self.config = config
        self.logger = colorlog.getLogger('mangekyou:pluginloader')
        self.logger.addHandler(self.config.handler)

        self.manager = PluginManager(categories_filter=self.config.categories_filter)
        self.manager.setPluginPlaces([self.config.plugins_folder])

        self.logger.debug(f"Searching for plugins in {self.config.plugins_folder}")

    def load_plugins(self) -> list:
        plugins = list()

        self.manager.collectPlugins()
        load = self.manager.getAllPlugins()
        for plugin in load:
            self.logger.debug(f"{plugin.name} loaded!")
            plugins.append(plugin)

        return plugins
