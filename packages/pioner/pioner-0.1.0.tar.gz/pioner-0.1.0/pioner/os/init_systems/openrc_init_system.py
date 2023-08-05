from re import findall

from pioner.errors import ParseStatusError, UnknownStatusError
from pioner.os.system import InitSystem, ServiceStatus, execute_shell


class OpenrcServiceStatus:
    STARTED = "started"
    STARTING = "starting"
    STOPPED = "stopped"
    STOPPING = "stopping"
    INACTIVE = "inactive"
    SCHEDULED = "scheduled"
    FAILED = "failed"

    @staticmethod
    def from_string(status: str) -> str:
        if status == "started":
            return OpenrcServiceStatus.STARTED

        if status == "starting":
            return OpenrcServiceStatus.STARTING

        if status == "stopped":
            return OpenrcServiceStatus.STOPPED

        if status == "stopping":
            return OpenrcServiceStatus.STOPPING

        if status == "inactive":
            return OpenrcServiceStatus.INACTIVE

        if status == "scheduled":
            return OpenrcServiceStatus.SCHEDULED

        if status == "failed":
            return OpenrcServiceStatus.FAILED

        raise UnknownStatusError()

    @staticmethod
    def to_status(status: str) -> str:
        if status == OpenrcServiceStatus.STARTED:
            return ServiceStatus.STARTED

        if status == OpenrcServiceStatus.STOPPED:
            return ServiceStatus.STOPPED

        if status == OpenrcServiceStatus.FAILED:
            return ServiceStatus.ERROR

        return ServiceStatus.OTHER


class OpenrcInitSystem(InitSystem):
    async def start(self, id: str) -> bool:
        if await self.status(id) != ServiceStatus.STOPPED:
            return False

        await execute_shell(f"rc-service {id} start")
        return True

    async def stop(self, id: str) -> bool:
        if await self.status(id) != ServiceStatus.STARTED:
            return False

        await execute_shell(f"rc-service {id} stop")
        return True

    async def restart(self, id: str) -> bool:
        if await self.status(id) != ServiceStatus.STARTED:
            return False

        await execute_shell(f"rc-service {id} restart")
        return True

    async def status(self, id: str) -> str:
        _, stdout, _ = await execute_shell(f"rc-service {id} status")
        status = OpenrcServiceStatus.from_string(stdout)
        return OpenrcServiceStatus.to_status(status)

    async def enable(self, id: str) -> bool:
        await execute_shell(f"rc-update add {id}")

    async def disable(self, id: str) -> bool:
        await execute_shell(f"rc-update del {id}")

    async def is_enabled(self, id: str) -> bool:
        _, stdout, _ = await execute_shell("rc-update show")
        statuses = findall(f" {id} \|", stdout)

        if len(statuses) not in (0, 1):
            raise ParseStatusError()

        return len(statuses) == 1
