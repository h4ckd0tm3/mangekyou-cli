import sys
import colorlog

from mangekyou import *
from pathlib import Path
from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    config_file = Path.home() / ".mangekyou" / "config.json"

    ap = ArgumentParser(
        description="OSINT Automation Framework - Dousatsugan."
    )

    ap.add_argument("--config", action="store", type=str, help="path to the config file to use",
                    default=str(config_file))
    ap.add_argument("--target", action="store", type=str,
                    help="Target folder, use 'mangekyou-tg' to generate a target folder", required=True)

    return ap.parse_args(sys.argv[1:])


def main():
    args = parse_args()

    colorlog.root.setLevel("INFO")
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s[%(name)s][%(levelname)s]: %(message)s'))

    logger = colorlog.getLogger('mangekyou:cli')
    logger.addHandler(handler)

    logger.info("Starting Mangekyou")

    try:
        config = Config(args.config, handler)
        target = str(Path.cwd() / args.target)
        man = Mangekyou(config, target)
        man.run()
    except Exception as e:
        logger.exception(e)
        logger.critical("exiting due to uncaught exception")
        sys.exit(2)


if __name__ == "__main__":
    main()
