from typing import List

from boundless import User
from pioner.context import get_distributive
from pioner.os.system import FileId


async def configure(
    user: User,
    *,
    port: int,
    server_private_key: str = None,
    server_public_key: str = None,
    client_public_keys: List[str] = None,
):
    await get_distributive().file_write_indirectly(
        FileId.SSH_CONFIG,
        "service/ssh/sshd_config.j2",
        port=port,
    )

    if server_private_key:
        await get_distributive().file_write_indirectly(
            FileId.SSH_SERVER_KEY_PRIVATE,
            "service/ssh/ssh_host_ed25519_key.j2",
            key=server_private_key,
        )

    if server_public_key:
        await get_distributive().file_write_indirectly(
            FileId.SSH_SERVER_KEY_PUBLIC,
            "service/ssh/ssh_host_ed25519_key.pub.j2",
            key=server_public_key,
        )

    if client_public_keys:
        await get_distributive().file_write_indirectly(
            FileId.SSH_CLIENT_KEYS,
            "service/ssh/authorized_keys.j2",
            keys=client_public_keys,
        )

    await get_distributive().service_reload("sshd")


async def status(
    user: User,
) -> str:
    return await get_distributive().service_status("sshd")


async def start(
    user: User,
):
    await get_distributive().service_start("sshd")


async def stop(
    user: User,
):
    await get_distributive().service_stop("sshd")
