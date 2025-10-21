import json
import atexit
import textwrap
import argparse
import logging.config
import logging.handlers
from pathlib import Path
from datetime import date

from nocover.ui import NCApp
from nocover.appinfo import APP_NAME, VERSION, DESCRIPTION

logger = logging.getLogger(__name__)

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(text=DESCRIPTION),
    )

    parser.add_argument(
        "--config", type=str, help="Path to config directory", default="/hcdb/"
    )

    levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log_level', default='INFO', choices=levels)

    parser.add_argument("--version", action="version", version=VERSION)

    return parser.parse_args()


def _get_the_logger(log_path: str) -> None:
    """
    Logging setup is based on James Murphy video
    https://www.youtube.com/watch?v=9L77QExPmI0

    Very helpful in setting this up
    """
    config_file = Path("src/nocover/config_files/logging_config.json")
    with open(config_file) as in_file:
        config = json.load(in_file)

    # Override the configDict value with value I want
    config["handlers"]["file"]["filename"] = log_path

    logging.config.dictConfig(config)

    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start() #ty: ignore
        atexit.register(queue_handler.listener.stop) #ty: ignore


def main():
    args = parse_args(argv=None)

    filename = f"{args.config}/logs/"
    Path.mkdir(Path(filename), exist_ok=True, parents=True)

    # SO EVERYONE KNOWS WHICH WAY THE MONTH AND DAY GO!
    today: date = date.today()
    full_logger_path = f"{filename}/NC_Y{today.year}_M{today.month}_D{today.day}.log"

    _get_the_logger(full_logger_path)

    if not Path(args.config).is_dir():
        logger.info(f"Making config dir @ {args.config}")
        output_file = Path(args.config)
        output_file.mkdir(exist_ok=True, parents=True)
    else:
        logger.info(f"Config dir exists @ {args.config}")

    app = NCApp(args.config)
    app.run()
