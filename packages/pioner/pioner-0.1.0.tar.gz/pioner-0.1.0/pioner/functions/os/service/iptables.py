from boundless import User

from pioner.context import get_distributive
from pioner.os.system import FileId


async def configure(
    user: User,
):
    await get_distributive().file_write_indirectly(
        FileId.IPTABLES,
        "service/iptables/iptables.j2",
    )
    await get_distributive().service_reload("iptables")


async def status(
    user: User,
) -> str:
    return await get_distributive().service_status("iptables")


async def start(
    user: User,
):
    await get_distributive().service_start("iptables")


async def stop(
    user: User,
):
    await get_distributive().service_stop("networking")
