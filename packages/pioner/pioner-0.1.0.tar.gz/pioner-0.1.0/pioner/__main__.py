from sys import stdout

from air_kit.logging import configure_loggers

from pioner.context import get_telemetry


class TelemetryStream:
    def __init__(
        self,
        is_stdout: bool = True,
        is_telemetry: bool = True,
    ):
        self.is_stdout = is_stdout
        self.is_telemetry = is_telemetry

    def write(self, data):
        if self.is_stdout:
            stdout.write(data)

        if self.is_telemetry:
            get_telemetry().enqueue(data)

    def flush(self):
        if self.is_stdout:
            stdout.flush()


configure_loggers(TelemetryStream(), "json")

from argparse import ArgumentParser
from logging import getLogger
from signal import SIGHUP, SIGTERM, SIGUSR1, SIGUSR2

logger = getLogger()

from .application import Application


def os(arguments):
    application = Application(
        arguments.host,
        arguments.port,
    )
    application.start()


def container(arguments):
    application = Application(
        arguments.host,
        arguments.port,
        is_container=True,
        command=arguments.command,
        signal_reload_full=arguments.signal_reload_full,
        signal_reload_partial=arguments.signal_reload_partial,
    )
    application.start()


def parse_arguments():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(required=True)

    parser_os = subparser.add_parser("os")
    parser_os.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
    )
    parser_os.add_argument(
        "--port",
        type=int,
        default=3000,
    )
    parser_os.set_defaults(handler=os)

    parser_container = subparser.add_parser("container")
    parser_container.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
    )
    parser_container.add_argument(
        "--port",
        type=int,
        default=3000,
    )
    parser_container.add_argument(
        "--command",
        type=str,
        required=True,
    )
    parser_container.add_argument(
        "--signal-reload-full",
        type=int,
        choices=[SIGTERM, SIGUSR1, SIGUSR2, SIGHUP],
        required=True,
    )
    parser_container.add_argument(
        "--signal-reload-partial",
        type=int,
        choices=[SIGTERM, SIGUSR1, SIGUSR2, SIGHUP],
        required=True,
    )
    parser_container.set_defaults(handler=container)

    arguments = parser.parse_args()
    arguments.handler(arguments)


def main():
    parse_arguments()


try:
    main()
except BaseException:
    logger.exception("Internal error.")
    exit(1)
