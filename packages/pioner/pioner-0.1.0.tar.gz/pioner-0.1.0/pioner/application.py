from asyncio import create_subprocess_exec, wait_for
from logging import getLogger
from multiprocessing import Queue
from signal import SIGHUP, SIGKILL, SIGTERM, SIGUSR1, SIGUSR2
from sys import stderr, stdout
from uuid import uuid4

from aiohttp import ClientSession
from aiohttp.web import middleware
from air_kit.application import Application as BaseApplication
from air_kit.logging import set_correlation_id
from air_kit.process import Process
from boundless import AioHttpServerTransport, Server

from pioner import functions
from pioner.context import set_application, set_distributive, set_telemetry
from pioner.os.distributive import Distributive

logger = getLogger()


@middleware
async def correlation_id_middleware(request, handler):
    set_correlation_id(uuid4().hex)
    return await handler(request)


class Application(BaseApplication):
    def __init__(
        self,
        host,
        port,
        is_container=False,
        command=None,
        signal_reload_full=None,
        signal_reload_partial=None,
    ):
        super().__init__("pioner")

        self.api = Api(host, port)

        if is_container:
            self.executing_process = ExecutingProcess(
                command,
                signal_reload_full,
                signal_reload_partial,
            )
        else:
            self.executing_process = None

        self.telemetry_process = TelemetryProcess("127.0.0.1", 9000)
        self.telemetry_process.start()

        set_application(self)
        set_distributive(Distributive())
        set_telemetry(self.telemetry_process)

    async def reload_full(self):
        if self.executing_process is None:
            return

        await self.executing_process.reload_full()
        logger.debug("Configuration reloaded.")

    async def reload_partial(self):
        if self.executing_process is None:
            return

        await self.executing_process.reload_partial()
        logger.debug("Configuration reloaded.")

    async def _on_start(self):
        if self.executing_process is not None:
            await self.executing_process.start()

        await self.api.start()

    async def _on_stop(self):
        await self.api.stop()

        if self.executing_process is not None:
            await self.executing_process.stop()

        self.telemetry_process.stop()


class Api:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.api = None

    async def start(self):
        self.api = Server(
            AioHttpServerTransport(
                self.host,
                self.port,
                [
                    correlation_id_middleware,
                ],
            ),
            functions,
        )
        await self.api.start()
        logger.debug("Rpc server started.")

    async def stop(self):
        pass


class ExecutingProcess:
    def __init__(
        self,
        command,
        signal_reload_full,
        signal_reload_partial,
        timeout=5,
    ):
        command = command.split(" ")
        self.program = command[0]
        self.arguments = command[1:]
        self.signal_reload_full = signal_reload_full
        self.signal_reload_partial = signal_reload_partial
        self.timeout = timeout
        self.process = None

    async def start(self):
        assert self.process is None, "Process already started."
        await self._create_process()
        logger.debug("Process started.")

    async def stop(self):
        assert self.process is not None, "Process not started."
        result = await self._destroy_process()
        logger.debug("Process stopped.")
        return result

    async def reload_full(self):
        assert self.process is not None, "Process not started."

        if self.signal_reload_full in [
            SIGUSR1,
            SIGUSR2,
            SIGHUP,
        ]:
            self.process.send_signal(self.signal_reload_full)
            return

        await self._destroy_process()
        await self._create_process()
        logger.debug("Process reloaded.")

    async def reload_partial(self):
        assert self.process is not None, "Process not started."

        if self.signal_reload_partial in [
            SIGUSR1,
            SIGUSR2,
            SIGHUP,
        ]:
            self.process.send_signal(self.signal_reload_partial)
            return

        await self._destroy_process()
        await self._create_process()
        logger.debug("Process reloaded.")

    async def _create_process(self):
        self.process = await create_subprocess_exec(
            self.program,
            *self.arguments,
            stdout=stdout,
            stderr=stderr,
        )

    async def _destroy_process(self):
        self.process.send_signal(SIGTERM)

        try:
            await wait_for(self.process.communicate(), timeout=self.timeout)
        except TimeoutError:
            try:
                self.process.send_signal(SIGKILL)
            except:
                pass

            return False

        return True


class TelemetryProcess(Process):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.queue = Queue()

        super().__init__("telemetry", period=3.0)

    def enqueue(self, data):
        self.queue.put(data)

    async def _on_start(self) -> None:
        pass

    async def _on_stop(self) -> None:
        await self._flush()

    async def _activity(self):
        await self._flush()

    async def _flush(self):
        if self.queue.empty():
            return

        buffer = []

        while not self.queue.empty():
            buffer.append(self.queue.get()[:-1])

        # TODO: check response ok
        # TODO: handle exceptions

        async with ClientSession() as session:
            async with session.post(
                f"http://{self.host}:{self.port}/logs",
                json={
                    "items": buffer,
                },
            ) as _:
                pass
