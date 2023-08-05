from ipaddress import ip_network
from typing import Dict, List

from dateutil.parser import isoparse
from pioner.os.file_hierarchies.alpine_file_hierarchy import AlpineFileHierarchy
from pioner.os.file_hierarchies.ubuntu_file_hierarchy import UbuntuFileHierarchy
from pioner.os.init_systems.initd_init_system import InitdInitSystem
from pioner.os.init_systems.openrc_init_system import OpenrcInitSystem
from pioner.os.system import (
    directories_list,
    execute_shell,
    file_exists,
    file_read,
    file_write,
)


class DistributiveId:
    UNKNOWN = "unknown"
    ALPINE = "alpine"
    UBUNTU = "ubuntu"
    DEBIAN = "debian"
    CENTOS = "centos"
    REDHAT = "redhat"
    # ...

    @staticmethod
    def from_string(distributive):
        if distributive == "alpine":
            return DistributiveId.ALPINE

        if distributive == "ubuntu":
            return DistributiveId.UBUNTU

        assert False, "Distributive not supported."


class Distributive:
    def __init__(self):
        with open("/etc/os-release", "rt") as handle:
            lines = handle.readlines()

        self.information = {}

        for line in lines:
            if not line:
                continue

            key, value = line.replace("\n", "").replace('"', "").split("=")
            self.information[key.lower()] = value

        assert "id" in self.information, "Malformed /etc/os-release."

    @property
    def id(self) -> str:
        return DistributiveId.from_string(self.information["id"])

    async def information_name(self) -> str:
        return self.information.get("pretty_name", None)

    async def information_version(self) -> str:
        return self.information.get("version_id", None)

    async def information_kernel(self) -> str:
        _, version, _ = await execute_shell("uname -r")
        return version.replace("\n", "")

    async def information_architecture(self) -> str:
        _, architecture, _ = await execute_shell("uname -m")
        return architecture.replace("\n", "")

    async def file_read_directly(
        self,
        file_path: str,
    ) -> str:
        return await file_read(file_path)

    async def file_read_indirectly(
        self,
        file_id: str,
    ) -> str:
        file_path = self._file_hierarchy.path(file_id)
        return await file_read(file_path)

    async def file_write_directly(
        self,
        file_path: str,
        template_path: str,
        **template_configuration,
    ) -> None:
        return await file_write(file_path, template_path, **template_configuration)

    async def file_write_indirectly(
        self,
        file_id: str,
        template_path: str,
        **template_configuration,
    ) -> None:
        file_path = self._file_hierarchy.path(file_id)
        return await file_write(file_path, template_path, **template_configuration)

    async def service_start(self, id: str) -> None:
        await self._init_system.start(id)

    async def service_stop(self, id: str) -> None:
        await self._init_system.stop(id)

    async def service_restart(self, id: str) -> str:
        await self._init_system.restart(id)

    async def service_reload(self, id: str) -> str:
        await self.service_stop(id)
        await self.service_start(id)

    async def service_status(self, id: str) -> str:
        return await self._init_system.status(id)

    async def service_enable(self, id: str) -> str:
        return await self._init_system.enable(id)

    async def service_disable(self, id: str) -> str:
        return await self._init_system.disable(id)

    # TODO: move
    async def network_interfaces_list(self) -> List[str]:
        return directories_list("/sys/class/net")

    # TODO: move
    async def network_interface_address(self, interface_id) -> Dict[str, str]:
        _, stdout, _ = await execute_shell(f"ip addr show {interface_id}")

        address = {
            "link": None,
            "ipv4": {
                "address": None,
                "network": None,
            },
            "ipv6": {
                "address": None,
                "network": None,
            },
        }

        for line in [line.strip() for line in stdout.split("\n")]:
            if line.startswith("link"):
                address["link"] = line.split(" ")[1]

            if line.startswith("inet "):
                line = line.split(" ")[1]
                address["ipv4"]["address"] = line.split("/")[0]
                address["ipv4"]["network"] = str(ip_network(line, strict=False))

            if line.startswith("inet6 "):
                line = line.split(" ")[1]
                address["ipv6"]["address"] = line.split("/")[0]
                address["ipv6"]["network"] = str(ip_network(line, strict=False))

        return address

    # TODO: move
    async def network_interface_information(self, interface_id: str) -> List[str]:
        prefix = f"/sys/class/net/{interface_id}"

        async def read_value(name):
            value = await file_read(f"{prefix}/{name}")
            return value.replace("\n", "")

        return {
            name: await read_value(name)
            for name in [
                # "addr_assign_type",
                # "address",
                # "addr_len",
                "broadcast",
                "carrier",
                # "carrier_changes",
                # "carrier_down_count",
                # "carrier_up_count",
                # "dev_id",
                # "dev_port",
                # "dormant",
                # "duplex",
                "flags",
                # "gro_flush_timeout",
                # "ifalias",
                # "ifindex",
                # "iflink",
                # "link_mode",
                "mtu",
                # "name_assign_type",
                # "napi_defer_hard_irqs",
                # "netdev_group",
                # "operstate",
                # "phys_port_id",
                # "phys_port_name",
                # "phys_switch_id",
                # "proto_down",
                # "speed",
                # "testing",
                "tx_queue_len",
                "type",
                # "uevent",
                # TODO: ...
            ]
        }

    # TODO: move
    async def network_interface_statistics(self, interface_id: str) -> List[str]:
        prefix = f"/sys/class/net/{interface_id}/statistics"

        async def read_value(name):
            value = await file_read(f"{prefix}/{name}")
            return value.replace("\n", "")

        return {
            name: await read_value(name)
            for name in [
                "collisions",
                "multicast",
                "rx_bytes",
                "rx_compressed",
                "rx_crc_errors",
                "rx_dropped",
                "rx_errors",
                "rx_fifo_errors",
                "rx_frame_errors",
                "rx_length_errors",
                "rx_missed_errors",
                "rx_nohandler",
                "rx_over_errors",
                "rx_packets",
                "tx_aborted_errors",
                "tx_bytes",
                "tx_carrier_errors",
                "tx_compressed",
                "tx_dropped",
                "tx_errors",
                "tx_fifo_errors",
                "tx_heartbeat_errors",
                "tx_packets",
                "tx_window_errors",
                # TODO: ...
            ]
        }

    # TODO: move
    async def network_dhcp_leases(self, interfaces) -> List[object]:
        leases = {}

        for interface in interfaces:
            path = f"/application/leases_{interface}"

            if not await file_exists(path):
                leases[interface] = []
                continue

            leases = {}

            for lease in (await file_read(path)).split("\n"):
                lease = lease.strip()

                if not lease:
                    continue

                lease = lease.split(" ")

                ip = lease[1]
                mac = lease[0]
                time = isoparse(lease[2])

                if mac in leases:
                    if leases[mac]["time"] > time:
                        continue

                leases[mac] = {
                    "ip": ip,
                    "mac": mac,
                    "time": time,
                }

            leases[interface] = list(
                [
                    {
                        "ip": lease["ip"],
                        "mac": lease["mac"],
                        "time": lease["time"].isoformat().replace("+00:00", "Z"),
                    }
                    for lease in leases.values()
                ]
            )

        return leases

    @property
    def _file_hierarchy(self):
        if self.id == DistributiveId.ALPINE:
            return AlpineFileHierarchy()

        if self.id == DistributiveId.UBUNTU:
            return UbuntuFileHierarchy()

        raise NotImplementedError("Distributive is not supported.")

    @property
    def _init_system(self):
        if self.id == DistributiveId.ALPINE:
            return OpenrcInitSystem()

        if self.id == DistributiveId.UBUNTU:
            return InitdInitSystem()

        raise NotImplementedError("Distributive is not supported.")
