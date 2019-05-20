import sys
from ..app import create_data_watchdog_instance
from ..wsgi import wsgi


cli_help_string = """
usage: dashb <subcommand> [...]

\033[95m
Command-line interface to the Dashboard backend.
\033[0m

Sub Commands:
  backend           Init a backend instance
  watchdog          Run data.csv watchdog
"""

subcommands = {
    "backend": "Init a backend instance",
    "watchdog": "Run data.csv watchdog",
}

class bcolors():
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def main():
    args = sys.argv[1:]
    try:
        arg_validator(args)
        if args[0] == "backend":
            wsgi()
        if args[0] == "watchdog":
            create_data_watchdog_instance()
        else:
            cli_help()
    except AssertionError:
        cli_help()


def arg_validator(args):
    """argument validator"""
    assert len(args) > 0, "No Sub Commands given"
    assert args[0] in subcommands.keys(), \
        "ERROR: unknown subcommands %s" % args[1]


def cli_help():
    print(cli_help_string)
    print(
        bcolors.FAIL + "ERROR:" + bcolors.ENDC +
        "\nInvalid argument"
    )


if __name__ == '__main__':
    main()