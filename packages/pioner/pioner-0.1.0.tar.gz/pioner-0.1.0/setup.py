from subprocess import run

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

with open("README.md", "r") as handle:
    long_description = handle.read()


service_openrc = """#!/sbin/openrc-run

start() {
    start-stop-daemon \
        --start \
        --exec python3 -m pioner os --host 127.0.0.1 --port 8080 \
        --pidfile /var/run/pioner.pid
}

stop() {
    start-stop-daemon \
        --stop \
        --pidfile /var/run/pioner.pid
}
"""


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        install.run(self)

        with open("/etc/init.d/pioner", "wt") as handle:
            handle.write(service_openrc)

        run("chmod +x /etc/init.d/pioner", shell=True)
        run("rc-update add pioner", shell=True)


configuration = dict(
    name="pioner",
    version="0.1.0",
    description="Hawk controller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[],
    author="air64",
    author_email="contact.air64@yandex.ru",
    maintainer=", ".join(
        ("air64 <contact.air64@yandex.ru>",),
    ),
    maintainer_email="contact.air64@yandex.ru",
    url="https://gitlab.com/air64/pioner",
    project_urls={
        "Gitlab": "https://gitlab.com/air64/pioner",
    },
    license="MIT",
    packages=find_packages(),
    package_data={
        "pioner": [
            "../templates/*/*/*",
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        "jinja2==2.11.3",
        "pyyaml==5.3.1",
        "python-dateutil==2.8.1",
        "air-kit~=0.1.1",
        "boundless~=0.1.1",
    ],
    include_package_data=True,
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
    },
)
setup(**configuration)
