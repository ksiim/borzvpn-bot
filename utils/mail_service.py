import asyncio
from functools import lru_cache
import logging
from typing import Iterable

from aiogram import Bot
from bot import bot as main_bot
from utils.utils import chunked


class MailService:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    async def send_mail_to_ids(self, text: str | None, ids: Iterable[int]) -> None:
        if not text:
            return

        for ids_group in chunked(ids, 5):
            await asyncio.gather(
                *(self.send_mail(text, telegram_id) for telegram_id in ids_group)
            )

    async def send_mail(self, text: str, telegram_id: int) -> bool:
        try:
            logging.info(f"sended mail to {telegram_id}")
            await self._bot.send_message(telegram_id, text)
            return True
        except Exception as exc:
            return False


@lru_cache(maxsize=1)
def get_mail_service() -> MailService:
    return MailService(main_bot)
