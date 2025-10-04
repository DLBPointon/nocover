import textwrap
import argparse
from pathlib import Path

from nocover.ui import NCApp

VERSION = "0.1.0"
DESCRIPTION = """
NOCOVER
--------
A TUI for your Hardcover experience, supporting offline business too.

"""

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="nocover",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(text = DESCRIPTION)
    )

    parser.add_argument( "--config", type=str, help="", default = "/hcdb/")

    return parser.parse_args()


def main():
    args = parse_args()

    if not Path(args.config).is_dir():
        print(f"Making config dir @ {args.config}")
        output_file = Path(args.config)
        output_file.mkdir(exist_ok=True, parents=True)

    app = NCApp(args.config)
    app.run()
