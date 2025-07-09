from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, FSInputFile, BufferedInputFile
)
import cairosvg
from sqlalchemy import delete

from bot import dp, bot

from models.dbs.orm import Orm
from models.dbs.models import *
from utils.wireguard import WireGuard

from .callbacks import *
from .markups import *
from .states import *


@dp.message(F.photo)
async def photo_handler(message: Message):
    await message.answer(
        text=f"<code>{message.photo[-1].file_id}</code>"
    )
    
@dp.message(F.video)
async def video_handler(message: Message):
    await message.answer(
        text=f"<code>{message.video.file_id}</code>"
    )


@dp.message(Command('start'))
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()

    await Orm.create_user(message)
    await send_start_message(message)
    
@dp.message(Command('delme'))
async def delme_message_handler(message: Message):
    async with WireGuard() as wg:
        clients = await wg.get_clients()
        clients_ids = [client['id'] for client in clients if client["name"] == str(message.from_user.id)]
        for client_id in clients_ids:
            await wg.delete_client(client_id)
            print(f"Deleted client with ID: {client_id}")


@dp.callback_query(F.data == "main_menu")
async def main_menu_callback_handler(callback: CallbackQuery):
    await send_start_message(callback)


async def send_start_message(message: Message):
    await bot.send_photo(
        photo=start_photo,
        chat_id=message.from_user.id,
        reply_markup=start_markup
    )


@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn_callback(callback: CallbackQuery):
    await callback.message.answer(
        text=choose_type_of_subscription_text,
        reply_markup=choose_type_of_subscription_markup
    )

@dp.callback_query(F.data == "help")
async def help_callback_handler(callback: CallbackQuery):
    await callback.message.answer(
        text=help_text,
        reply_markup=help_markup
    )


@dp.callback_query(F.data == "my_subscription")
async def my_subscription_callback_handler(callback: CallbackQuery):
    end_of_subscription_date = await Orm.get_end_of_subscription(callback.from_user.id)
    user = await Orm.get_user_by_telegram_id(callback.from_user.id)
    wg = WireGuard()
    user_config_path = wg.get_user_config_path(user)
    if end_of_subscription_date:
        text = f"Ваша подписка активна до {end_of_subscription_date.strftime('%d.%m.%Y')}"
        await callback.message.answer_document(
            document=FSInputFile(user_config_path),
            caption=text,
            reply_markup=main_menu_markup
        )
    else:
        text = 'Похоже у вас еще нет подписки'
        await callback.message.answer(
            text=text,
            reply_markup=main_menu_markup
        )


@dp.message(Command('qwe'))
async def qwe_message(message: Message):
    await Orm.kill_date(message.from_user.id)
    
    
@dp.callback_query(lambda callback: callback.data.startswith('contype_'))
async def connection_type_handler(callback: CallbackQuery):
    connection_type = callback.data.split('_')[1]
    
    match connection_type:
        case 'qr':
            await proccess_qr_code_connection(callback.from_user.id)
        case 'config':
            await proccess_config_connection(callback.from_user.id)
    
    
async def proccess_qr_code_connection(telegram_id: int) -> str:
    user = await Orm.get_user_by_telegram_id(telegram_id)
    client_id = user.client_id
    async with WireGuard() as wg:
        qr_bytes = await wg.get_qrcode(client_id)
        qr_png_bytes = cairosvg.svg2png(bytestring=qr_bytes)

        qr_photo = BufferedInputFile(qr_png_bytes, filename="qrcode.png")
        
    await bot.send_photo(
        chat_id=telegram_id,
        photo=qr_photo,
    )
    
    await bot.send_video(
        chat_id=telegram_id,
        video=qr_ios_video,
        caption=qr_connection_text,
        reply_markup=main_menu_markup
    )
        
        
async def proccess_config_connection(telegram_id: int) -> str:
    user = await Orm.get_user_by_telegram_id(telegram_id)
    
    client_id = user.client_id
    async with WireGuard() as wg:
        config_bytes = await wg.get_configuration_file(client_id)
        config_file = BufferedInputFile(config_bytes, filename="wireguard.conf")
    
    await bot.send_document(chat_id=telegram_id, document=config_file)
    
    await bot.send_video(
        chat_id=telegram_id,
        video=conf_ios_video,
        caption=config_connection_text,
        reply_markup=main_menu_markup
    )

# @dp.message(Command('asd'))
# async def asd_message_handler(message: Message):
#     wg = WireGuard()
#     user = await Orm.get_user_by_telegram_id(message.from_user.id)
#     path, public_key = wg.create_user_config(user)
#     await Orm.update_public_key(user.id, public_key)
#     file = FSInputFile(path=path)
#     await message.answer_document(file)
#     wg.delete_user_config(user)

# @dp.message(Command('zxc'))
# async def zxc_message_handler(message: Message):
#     wg = WireGuard()
#     user = await Orm.get_user_by_telegram_id(message.from_user.id)
#     user_public_key = user.public_key
#     wg.remove_peer_from_server_config(user_public_key)