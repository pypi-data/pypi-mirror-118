from boundless import User

from pioner.context import get_application, get_distributive


async def configure(
    user: User,
    *,
    general: dict,
    templates: dict,
    transports: list,
):
    await get_distributive().file_write_directly(
        "/application/configuration/options/general.yaml",
        "container/homebrew/avalanche_coordinator/general.yaml.j2",
        configuration=general,
    )

    await get_distributive().file_write_directly(
        "/application/configuration/options/templates.yaml",
        "container/homebrew/avalanche_coordinator/templates.yaml.j2",
        configuration=templates,
    )

    await get_distributive().file_write_directly(
        "/application/configuration/options/transports.yaml",
        "container/homebrew/avalanche_coordinator/transports.yaml.j2",
        configuration=transports,
    )

    await get_application().reload_partial()
