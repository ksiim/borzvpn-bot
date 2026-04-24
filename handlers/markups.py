from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot

from .callbacks import *


prices = {
    1: 299,
    6: 799,
    12: 1499,
}

start_photo = 'AgACAgIAAxkBAANYaGV5HF3BvEAYsAdUgKNfDzCKA5MAArf3MRsryDBL-Y55BCvlqDcBAAMCAAN5AAM2BA'

choose_type_of_subscription_text = """<b>1️⃣ Выбери нужный тариф ниже👇🏻
2️⃣ Произведи оплату
3️⃣ Установи VPN на свое устройство </b>

❗️После оплаты выдадим приложение, которое доступно для установки на Iphone, Android, ПК, macOs

💡Доступ выдается на телефон, компьютер, планшет и телевизор AndroidTV"""

help_text = """<b>1)Для работы VPN необходимо скачать приложение WireGuard💚</b>
Оно есть: 
App Store 
Google play 
А также на ПК

2)Открыть приложение WireGuard и нажать кнопку «+», далее кнопка (по середине) 
<b>Создать из QR-кода 
Открываете оплаченный и полученный  вами QR-код 
Вкл/выкл в настройках телефона</b>
"""

async def generate_start_text(message):
    return "Чем могу помочь?"

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
                    text="Оплатить 💳",
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
                    callback_data=f"buy_vpn"
                )
            ]
        ]
    )
    
conf_ios_video = 'BAACAgIAAxkBAAIBrmhucP0a-KmW2nGqTK-HepBPTT6RAAJydAACFM14S2Z0cbe_Me0QNgQ'
qr_ios_video = 'BAACAgIAAxkBAAIBsGhucRMCOjWEMFEp7GZt4ctYDK5nAAJ2dAACFM14Swe0rBGAM-AtNgQ'


type_of_connection_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="QR-код (для доп. устройств)",
            callback_data="contype_qr"
        )],
        [InlineKeyboardButton(
            text="Файл конфигурации (на ваше устройство)",
            callback_data="contype_config"
        )]
    ]
)

qr_connection_text = 'Вот инструкция по подключению к VPN через QR-код'
config_connection_text = 'Вот инструкция по подключению к VPN через файл конфигурации'


choose_type_of_subscription_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'1 месяц - {prices[1]}р💚',
                callback_data='buy_vpn_:1'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'6 месяцев - {prices[6]}р💚',
                callback_data='buy_vpn_:6'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'12 месяцев - {prices[12]}р💚',
                callback_data='buy_vpn_:12'
            )
        ],
        [
            InlineKeyboardButton(
                text='Главное меню🛡',
                callback_data='main_menu'
            )
        ]
    ]
)


start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Купить подписку VPN💚 ",
                callback_data='buy_vpn'
            )
        ],
        [
            InlineKeyboardButton(
                text="Продлить подписку VPN🔋",
                callback_data='buy_vpn'
            )
        ],
        [
            InlineKeyboardButton(
                text='Помощь 📲',
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

help_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Поддержка',
                url='t.me/TurboOpel'
            )
        ],
        [
            InlineKeyboardButton(
                text='Главное меню🛡',
                callback_data='main_menu'
            )
        ]
    ]
)

main_menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Главное меню🛡',
                callback_data='main_menu'
            )
        ]
    ]
)