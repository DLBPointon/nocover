import textwrap
import argparse
import logging
from pathlib import Path

from nocover.ui import NCApp
from nocover.appinfo import APP_NAME, VERSION, DESCRIPTION


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(text=DESCRIPTION),
    )

    parser.add_argument(
        "--config", type=str, help="Path to config directory", default="/hcdb/"
    )

    parser.add_argument(
        "--log_level", choices=["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    )

    parser.add_argument("--version", action="version", version=VERSION)

    return parser.parse_args()


def main():
    args = parse_args(argv=None)

    if not Path(args.config).is_dir():
        print(f"Making config dir @ {args.config}")
        output_file = Path(args.config)
        output_file.mkdir(exist_ok=True, parents=True)

    app = NCApp(args.config)
    app.run()
