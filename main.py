import asyncio

from bot import dp, bot

import logging

import handlers

from models.databases import create_database
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.tasks import delete_unsubscribed_people
from utils.wireguard import WireGuard


logging.basicConfig(level=logging.INFO)

async def main():
    initialize_scheduler()
    await create_database()
    await dp.start_polling(bot)
    
def initialize_scheduler():
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(delete_unsubscribed_people, 'cron', hour=0)
    scheduler.add_job(delete_unsubscribed_people, 'interval', seconds=10)
    scheduler.start()

async def main():
    await create_database()
    initialize_scheduler()
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())