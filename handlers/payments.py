import asyncio

from aiogram.types import (
    Message, CallbackQuery
)
from aiogram import F

from models.dbs.orm import Orm

from bot import dp, bot

from utils.payments import YooPay

from handlers.markups import *
from utils.wireguard import WireGuard

@dp.callback_query(lambda callback: callback.data.startswith("buy_vpn_:") or callback.data.startswith("renew_vpn_:"))
async def get_period(callback: CallbackQuery):
    await callback.message.delete()
    
    period = int(callback.data.split(":")[-1])
    
    total_amount = prices[period]
    
    answer = await callback.message.answer(
        text=f"Вы выбрали VPN на {period} {await incline_by_period(period)}. Цена {total_amount}₽",
    )
    await card_callback(
        telegram_id=callback.from_user.id,
        period=period,
        total_amount=total_amount,
        type_=callback.data.split("_")[0]
    )
    await asyncio.sleep(10)
    await answer.delete()

async def card_callback(telegram_id=None, period=None, total_amount=None, type_=None):
    yoopay = YooPay()
    response = await yoopay.create_payment(
        amount=total_amount,
        period=period,
        telegram_id=telegram_id,
    )
    payment_id = response.id
    payment_link = response.confirmation.confirmation_url
    
    await bot.send_message(
        chat_id=telegram_id,
        text="Совершите оплату по ссылке ниже",
        reply_markup=await generate_payment_keyboard(payment_link=payment_link, payment_id=payment_id, type_=type_)
    )
    
@dp.callback_query(lambda callback: callback.data.startswith("check_payment"))
async def check_payment_callback(callback: CallbackQuery):
    _, payment_id = callback.data.split(":")
    payment = await YooPay.payment_success(payment_id)
    if payment:
        answer = await process_successful_payment(callback, payment)
    else:
        answer = await callback.message.answer("Оплата не прошла")
        
    await asyncio.sleep(3)
    await answer.delete()
    
async def process_successful_payment(callback: CallbackQuery, payment):
    await callback.message.delete()
    answer = await callback.message.answer("Оплата прошла успешно!")
    user = await Orm.get_user_by_telegram_id(callback.from_user.id)
    months = payment.metadata['period']
    result = await Orm.add_subscription_months(user.telegram_id, months)
    user = await Orm.get_user_by_telegram_id(callback.from_user.id)
    
    if result == 'new':
        await add_user_config(callback.from_user.id)
    
    await callback.message.answer(
        text=f"Благодарим за покупку! Ваша подписка активна до {user.end_of_subscription.strftime('%d.%m.%Y')}\n\nВыберите более удобный для вас вариант подключения",
        reply_markup=type_of_connection_markup
    )

    return answer

async def add_user_config(telegram_id):
    user = await Orm.get_user_by_telegram_id(telegram_id)
    async with WireGuard() as wg:
        # Создаем клиента (в ответе будет только {"success": true})
        await wg.create_client(user.telegram_id)
        
        # Получаем список клиентов и ищем нужного по имени (telegram_id)
        clients = await wg.get_clients()
        client = next((c for c in clients if c["name"] == str(user.telegram_id)), None)
        if not client:
            raise Exception("Не удалось найти созданного клиента после create_client")
        
        # Включаем клиента
        await wg.enable_client(client["id"])

    # Сохраняем client_id в БД
    await Orm.update_client_id(user.telegram_id, client["id"])
