from abc import ABC, abstractmethod
from asyncio import create_subprocess_exec, create_subprocess_shell, subprocess
from json import dumps as json_dump
from os import walk
from os.path import exists
from site import getsitepackages
from typing import List, Tuple

from jinja2 import Environment, FileSystemLoader
from yaml import dump as yaml_dump


class FileId:
    HOSTNAME = "hostname"
    SYSCTL = "sysctl"
    SUDO = "sudo"
    SSH_CONFIG = "ssh_config"
    SSH_SERVER_KEY_PRIVATE = "ssh_server_key_private"
    SSH_SERVER_KEY_PUBLIC = "ssh_server_key_public"
    SSH_CLIENT_KEYS = "ssh_client_keys"
    INTERFACES = "interfaces"
    WIFI = "wifi"
    IPTABLES = "iptables"


class FileHierarchy(ABC):
    @abstractmethod
    def path(self, file_id: int) -> str:
        pass


class ServiceStatus:
    STARTED = "started"
    STOPPED = "stopped"
    ERROR = "error"
    OTHER = "other"


class InitSystem(ABC):
    @abstractmethod
    async def start(self, id: str) -> bool:
        pass

    @abstractmethod
    async def stop(self, id: str) -> bool:
        pass

    @abstractmethod
    async def restart(self, id: str) -> bool:
        pass

    @abstractmethod
    async def status(self, id: str) -> str:
        pass

    @abstractmethod
    async def enable(self, id: str) -> bool:
        pass

    @abstractmethod
    async def disable(self, id: str) -> bool:
        pass

    @abstractmethod
    async def is_enabled(self, id: str) -> bool:
        pass


async def file_read(
    file_path: str,
) -> str:
    with open(file_path, "rt") as handle:
        return handle.read()


async def file_write(
    file_path: str,
    template_path: str,
    **template_configuration,
) -> None:
    environment = Environment(
        loader=FileSystemLoader(
            [
                "templates",
            ]
            + [f"{path}/templates" for path in getsitepackages()]
        ),
    )
    environment.filters["json"] = lambda data: json_dump(data, indent=4)
    environment.filters["yaml"] = lambda data: yaml_dump(data, indent=2)

    content = environment.get_template(template_path).render(**template_configuration)

    with open(file_path, "wt") as handle:
        handle.write(content)


async def file_exists(
    file_path: str,
) -> str:
    return exists(file_path)


async def execute_shell(command: str) -> Tuple[int, str, str]:
    process = await create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if stdout:
        stdout = stdout.decode()

    if stderr:
        stderr = stderr.decode()

    return process.returncode, stdout, stderr


async def execute_program(program: str, *args) -> Tuple[int, str, str]:
    process = await create_subprocess_exec(
        program,
        *args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if stdout:
        stdout = stdout.decode()

    if stderr:
        stderr = stderr.decode()

    return process.returncode, stdout, stderr


def format_output(output: str) -> str:
    return output.strip("\n").replace("\n", "\\n")


def files_list(directory: str) -> List[str]:
    for (_, _, file_names) in walk(directory):
        return file_names


def directories_list(directory: str) -> List[str]:
    for (_, directory_names, _) in walk(directory):
        return directory_names
