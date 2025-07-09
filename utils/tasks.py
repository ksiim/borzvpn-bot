

from models.dbs.models import User
from models.dbs.orm import Orm
from utils.wireguard import WireGuard
from bot import bot
from handlers.markups import main_menu_markup


async def delete_unsubscribed_people():
    users = await Orm.get_users_with_ended_subscription()
    async with WireGuard() as wg:
        for user in users:
            await disconnect_user(user, wg)
    
async def disconnect_user(user: User, wg: WireGuard):
    await Orm.unsubscribe_user(user.telegram_id)
    await wg.delete_client(user.client_id)
    await bot.send_message(
        chat_id=user.telegram_id,
        text=f"Ваш VPN был отключен, так как срок подписки истек. "
             f"Если вы хотите продолжить пользоваться VPN, "
             f"вы можете <b>подписаться</b> на него снова.",
        parse_mode='HTML',
        reply_markup=main_menu_markup
    )
    