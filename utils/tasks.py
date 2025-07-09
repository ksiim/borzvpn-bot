

from models.dbs.models import User
from models.dbs.orm import Orm
from utils.wireguard import WireGuard


async def delete_unsubscribed_people():
    users = await Orm.get_users_with_ended_subscription()
    async with WireGuard() as wg:
        for user in users:
            await disconnect_user(user, wg)
    
async def disconnect_user(user: User, wg: WireGuard):
    await Orm.unsubscribe_user(user.telegram_id)
    await wg.delete_client(user.client_id)