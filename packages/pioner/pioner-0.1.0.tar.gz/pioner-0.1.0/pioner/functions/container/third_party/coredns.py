from boundless import User

from pioner.context import get_application, get_distributive


async def configure(
    user: User,
    *,
    configuration: dict,
):
    await get_distributive().file_write_directly(
        "/application/configuration.conf",
        "container/third_party/coredns/configuration.conf.j2",
    )
    await get_application().reload_full()
