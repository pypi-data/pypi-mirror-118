from logging import getLogger
from re import findall

from pioner.errors import ParseStatusError, UnknownStatusError
from pioner.os.system import InitSystem, ServiceStatus, execute_shell, format_output

logger = getLogger(__name__)


class InitdServiceStatus:
    RUNNING = "running"
    DEAD = "dead"

    @staticmethod
    def from_string(status: str) -> str:
        if status == "running":
            return InitdServiceStatus.RUNNING

        if status == "dead":
            return InitdServiceStatus.DEAD

        raise UnknownStatusError()

    @staticmethod
    def to_status(status: str) -> str:
        if status == InitdServiceStatus.RUNNING:
            return ServiceStatus.STARTED

        if status == InitdServiceStatus.DEAD:
            return ServiceStatus.STOPPED

        return ServiceStatus.OTHER


class InitdInitSystem(InitSystem):
    async def start(self, id: str) -> bool:
        code, _, stderr = await execute_shell(f"service {id} start")

        if code != 0:
            logger.error(format_output(stderr))

        return code == 0

    async def stop(self, id: str) -> bool:
        code, _, stderr = await execute_shell(f"service {id} stop")

        if code != 0:
            logger.error(format_output(stderr))

        return code == 0

    async def restart(self, id: str) -> bool:
        code, _, stderr = await execute_shell(f"service {id} restart")

        if code != 0:
            logger.error(format_output(stderr))

        return code == 0

    async def status(self, id: str) -> str:
        code, stdout, stderr = await execute_shell(f"service {id} status")

        if code != 0:
            logger.error(format_output(stderr))
            raise ParseStatusError()

        statuses = findall(r"Active: [a-z]+ \(([a-z]+)\)", stdout)

        if len(statuses) != 1:
            logger.error(
                f"Stdout not match regex, service = `{id}`, stdout = `{format_output(stdout)}`.",
            )
            raise ParseStatusError()

        status = InitdServiceStatus.from_string(statuses[0])
        return InitdServiceStatus.to_status(status)

    async def enable(self, id: str) -> bool:
        code, _, stderr = await execute_shell(f"systemctl enable {id}")

        if code != 0:
            logger.error(format_output(stderr))

        return code == 0

    async def disable(self, id: str) -> bool:
        code, _, stderr = await execute_shell(f"systemctl disable {id}")

        if code != 0:
            logger.error(format_output(stderr))

        return code == 0

    async def is_enabled(self, id: str) -> bool:
        code, stdout, stderr = await execute_shell(f"service {id} status")

        if code != 0:
            logger.error(format_output(stderr))
            raise ParseStatusError()

        statuses = findall(r"Active: ([a-z])+)", stdout)

        if len(statuses) != 1:
            logger.error(
                f"Stdout not match regex, service = `{id}`, stdout = `{format_output(stdout)}`.",
            )
            raise ParseStatusError()

        return statuses[0] == "active"
