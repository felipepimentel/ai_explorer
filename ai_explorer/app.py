import logging

from .config import Config

logging.basicConfig(
    level=Config.LOGGING_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    if Config.GUI_ENABLED:
        from .gui import start_gui

        start_gui()
    elif Config.API_ENABLED:
        from .api import start_api

        start_api()
    else:
        from .cli import cli

        cli()


if __name__ == "__main__":
    main()
