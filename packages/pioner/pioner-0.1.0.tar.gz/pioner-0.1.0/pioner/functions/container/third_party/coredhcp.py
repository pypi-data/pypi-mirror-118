from ipaddress import ip_network

from boundless import User

from pioner.context import get_application, get_distributive


async def configure(
    user: User,
    *,
    time: int,
    interfaces: dict,
):
    # Add time attribute to static leases.
    for interface in interfaces.keys():
        interfaces[interface]["mask"] = str(
            _cidr_to_network(
                interfaces[interface]["ip"],
                interfaces[interface]["prefix"],
            ).netmask
        )

        for lease in interfaces[interface]["leases"]:
            lease["time"] = "1970-01-01T00:00:00Z"

    # # Merge dynamic and static leases.
    # leases = await get_distributive().network_dhcp_leases(
    #     interfaces.keys(),
    # )
    # for interface in interfaces.keys():
    #     interfaces[interface]["leases"] += leases[interface]

    # Render configuration templates.
    await get_distributive().file_write_directly(
        "/application/configuration.yaml",
        "container/third_party/coredhcp/configuration.yaml.j2",
        time=time,
        interfaces=interfaces,
    )

    for interface, configuration in interfaces.items():
        await get_distributive().file_write_directly(
            f"/application/leases_{interface}",
            "container/third_party/coredhcp/leases.j2",
            leases=configuration["leases"],
        )

    # Reload coredhcp.
    await get_application().reload_full()


async def leases(
    user: User,
    interfaces,
):
    return await get_distributive().network_dhcp_leases(
        interfaces,
    )


def _cidr_to_network(ip, prefix):
    return ip_network(
        f"{ip}/{prefix}",
        strict=False,
    )
