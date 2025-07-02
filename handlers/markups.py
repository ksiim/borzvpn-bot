from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot

from .callbacks import *


prices = {
    3: 100,
    6: 200,
    12: 400
}

help_photo = 'AgACAgIAAxkBAAMRaGTxaTpxfmzzHCST3XgVR82pkUYAAgvxMRvz2ShLcdYHnygF1AABAQADAgADeAADNgQ'
start_photo = 'AgACAgIAAxkBAAMRaGTxaTpxfmzzHCST3XgVR82pkUYAAgvxMRvz2ShLcdYHnygF1AABAQADAgADeAADNgQ'

choose_type_of_subscription_text = """1️⃣ Выбери нужный тариф ниже👇🏻
2️⃣ Произведи оплату
3️⃣ Установи VPN на свое устройство 

❗️После оплаты выдадим приложение, которое доступно для установки на Iphone, Android, ПК, macOs

💡Доступ выдается на телефон, компьютер, планшет и телевизор AndroidTV"""

help_text = """Для работы VPN необходимо скачать WireGuard приложение из Google Play / App Store, также приложение есть на ПК.

Открыть приложение WireGuard и нажать кнопку «+», далее «импорт из файла или архива» выбрать ранее полученный файл от бота после покупки подписки. Для выключения или включения VPN нажимайте на ползунок.

При возникновении проблем свяжитесь с поддержкой"""

async def generate_start_text(message):
    return f"Чем могу помочь?"

async def incline_by_period(period):
    if period == 1:
        return "месяц"
    elif period in (2, 3, 4):
        return "месяца"
    else:
        return "месяцев"
    
async def generate_payment_keyboard(payment_link: str, payment_id: str, type_=None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оплатить",
                    url=payment_link,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Проверить оплату/Получить VPN",
                    callback_data=f"check_payment:{payment_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=f"{type_}_vpn"
                )
            ]
        ]
    )

choose_type_of_subscription_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'🟢3 мес - {prices[3]}р',
                callback_data='buy_vpn_:3'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'🔵6 мес - {prices[6]}р',
                callback_data='buy_vpn_:6'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'🟣12 мес - {prices[12]}р',
                callback_data='buy_vpn_:12'
            )
        ],
        [
            InlineKeyboardButton(
                text='🛡Главное меню',
                callback_data='main_menu'
            )
        ]
    ]
)


start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔌Купить\продлить подписку VPN ",
                callback_data='buy_vpn'
            )
        ],
        [
            InlineKeyboardButton(
                text='🛟Помощь',
                callback_data='help'
            )
        ],
        # [
        #     InlineKeyboardButton(
        #         text='Моя подписка',
        #         callback_data='my_subscription'
        #     )
        # ]
    ]
)

main_menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='🛡Главное меню',
                callback_data='main_menu'
            )
        ]
    ]
)