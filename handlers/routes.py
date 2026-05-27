import asyncio
import aiohttp

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

router = Router()

subscribers = set()


async def notifier(bot: Bot):  # исправлено: было notfier
    while True:
        await asyncio.sleep(10)
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, "Ваше стандартное сообщение")
                except Exception:
                    pass


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет!\n"
        "Я могу помочь с рассылкой!\n\n"
        "Команды:\n"
        "/subscribe - подписаться на уведомление\n"
        "/unsubscribe - отписка\n"
        "/subscribers - список подписчиков"
    )


@router.message(Command("subscribe"))
async def subscribe(message: Message):
    user_id = message.from_user.id

    if user_id in subscribers:
        await message.answer("Вы уже подписаны!")
        return

    subscribers.add(user_id)  # исправлено: не добавлялся в set
    await message.answer("Вы подписались!")


@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):  # исправлено: было дублирование имени subscribe
    user_id = message.from_user.id
    subscribers.discard(user_id)
    await message.answer("Вы отписались!")


@router.message(Command("subscribers"))
async def subscribers_list(message: Message):  # исправлено: странное имя функции
    if not subscribers:
        await message.answer("Пока никого нет")
        return

    text = "Подписчики:\n"
    for uid in subscribers:
        text += f"{uid}\n"

    await message.answer(text)