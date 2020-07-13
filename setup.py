import os

from git import Repo
from pathlib import Path
from setuptools import setup
from mangekyou.version import __version__

from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        dotfolder = Path.home() / ".mangekyou"
        dotfolder.mkdir(parents=True, exist_ok=True)

        config_file = dotfolder / "config.json"
        if not config_file.is_file():
            os.system(f"cp data/sampleconfig.json {str(config_file)}")

        plugins_folder = dotfolder / "plugins"
        plugins_folder.mkdir(parents=True, exist_ok=True)

        if not any(plugins_folder.iterdir()):
            Repo.clone_from("https://github.com/h4ckd0tm3/mangekyou-plugins.git", f"{str(plugins_folder)}")

        temp_folder = dotfolder / "temp"
        temp_folder.mkdir(parents=True, exist_ok=True)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        develop.run(self)
        dotfolder = Path.home() / ".mangekyou"
        dotfolder.mkdir(parents=True, exist_ok=True)

        config_file = dotfolder / "config.json"
        if not config_file.is_file():
            os.system(f"cp data/sampleconfig.json {str(config_file)}")

        plugins_folder = dotfolder / "plugins"
        plugins_folder.mkdir(parents=True, exist_ok=True)

        if not any(plugins_folder.iterdir()):
            Repo.clone_from("https://github.com/h4ckd0tm3/mangekyou-plugins.git", f"{str(plugins_folder)}")

        temp_folder = dotfolder / "temp"
        temp_folder.mkdir(parents=True, exist_ok=True)


with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("mangekyou/version.py", "r") as f:
    exec(f.read(), globals())

setup(
    name="mangekyou",
    description="OSINT Automation Framework - Dousatsugan.",
    version=__version__,
    author="Marcel Schnideritsch",
    packages=["mangekyou"],
    entry_points={
        "console_scripts": [
            "mangekyou = mangekyou.cli.main:main",
            "mangekyou-tg = mangekyou.util.targetgenerator:main"
        ]
    },
    package_data={
        "mangekyou": ["py.typed"]
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    python_requires=">=3.7",
    install_requires=requirements
)
