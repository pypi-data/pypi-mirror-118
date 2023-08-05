from boundless import User

from pioner.context import get_application, get_distributive


async def configure(
    user: User,
    *,
    port: int,
    exit_nodes: str,
):
    await get_distributive().file_write_directly(
        "/application/torrc",
        "container/third_party/tor_socks_proxy/torrc.j2",
        port=port,
        exit_nodes=exit_nodes,
    )
    # await get_application().reload_full()
