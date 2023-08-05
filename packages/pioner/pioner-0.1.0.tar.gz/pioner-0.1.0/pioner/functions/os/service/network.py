from ipaddress import ip_network

from boundless import User

from pioner.context import get_distributive
from pioner.os.system import FileId


async def configure(
    user: User,
    *,
    interfaces: list,
    wifi: dict,
):
    for interface in interfaces:
        if "prefix" not in interface:
            continue

        interface["mask"] = str(
            _cidr_to_network(
                interface["ip"],
                interface["prefix"],
            ).netmask
        )

    # Network interfaces.
    await get_distributive().file_write_indirectly(
        FileId.INTERFACES,
        "service/network/interfaces.j2",
        interfaces=interfaces,
    )
    await get_distributive().service_restart(
        "networking",
    )

    # Wi-Fi.
    if wifi:
        await get_distributive().file_write_indirectly(
            FileId.WIFI,
            "service/network/hostapd.conf.j2",
            wifi=wifi,
        )
        await get_distributive().service_restart(
            "hostapd",
        )


async def status(
    user: User,
) -> str:
    return await get_distributive().service_status("networking")


async def start(
    user: User,
):
    await get_distributive().service_start("iptables")


async def stop(
    user: User,
):
    await get_distributive().service_stop("networking")


def _cidr_to_network(ip, prefix):
    return ip_network(
        f"{ip}/{prefix}",
        strict=False,
    )
