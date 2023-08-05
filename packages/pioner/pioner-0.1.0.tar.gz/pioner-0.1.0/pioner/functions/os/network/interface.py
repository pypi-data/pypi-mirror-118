from boundless import User

from pioner.context import get_distributive


async def list_(
    user: User,
):
    distributive = get_distributive()
    return await distributive.network_interfaces_list()


# async def addresses(
#     user: User,
# ):
#     distributive = get_distributive()
#     statistics = {
#         interface_id: await distributive.network_interface_address(interface_id)
#         for interface_id in await distributive.network_interfaces_list()
#     }
#     return statistics


# async def information(
#     user: User,
# ):
#     distributive = get_distributive()
#     statistics = {
#         interface_id: await distributive.network_interface_information(interface_id)
#         for interface_id in await distributive.network_interfaces_list()
#     }
#     return statistics


async def statistics(
    user: User,
) -> dict:
    distributive = get_distributive()
    statistics = {
        interface_id: await distributive.network_interface_statistics(interface_id)
        for interface_id in await distributive.network_interfaces_list()
    }
    return statistics
