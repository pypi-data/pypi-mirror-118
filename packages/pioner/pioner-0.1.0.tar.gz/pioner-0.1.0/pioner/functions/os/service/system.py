from boundless import User

from pioner.context import get_distributive
from pioner.os.system import FileId, ServiceStatus, execute_shell


async def configure(
    user: User,
):
    await get_distributive().file_write_indirectly(
        FileId.HOSTNAME,
        "service/system/hostname.j2",
        hostname="hawk",
    )

    await get_distributive().file_write_indirectly(
        FileId.SYSCTL,
        "service/system/sysctl.conf.j2",
    )

    await get_distributive().file_write_indirectly(
        FileId.SUDO,
        "service/system/sudoers.j2",
    )

    await execute_shell("sysctl -p /etc/sysctl.conf")


async def status(
    user: User,
) -> str:
    return ServiceStatus.STARTED


async def start(
    user: User,
):
    pass


async def stop(
    user: User,
):
    pass
