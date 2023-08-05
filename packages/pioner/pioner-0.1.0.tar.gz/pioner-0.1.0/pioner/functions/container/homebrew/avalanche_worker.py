from boundless import User

from pioner.context import get_application, get_distributive


async def configure(
    user: User,
    *,
    general: dict,
):
    await get_distributive().file_write_directly(
        "/application/configuration/options/general.yaml",
        "container/homebrew/avalanche_worker/general.yaml.j2",
        configuration=general,
    )

    await get_application().reload_partial()
