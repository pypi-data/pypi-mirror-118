from boundless import User

from pioner.context import get_distributive
from pioner.os.system import FileId


async def debug(
    user: User,
):
    await get_distributive().file_write_indirectly(
        FileId.SYSCTL, "service/sysctl/sysctl.conf.j2", x={"a": {"b": 1}}
    )


async def information(
    user: User,
):
    distributive = get_distributive()
    return {
        "name": await distributive.information_name(),
        "version": await distributive.information_version(),
        "kernel": await distributive.information_kernel(),
        "architecture": await distributive.information_architecture(),
    }
