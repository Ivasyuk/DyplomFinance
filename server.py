"""Сервер Telegram"""
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
from categories import Categories
from middlewares import AccessMiddleware


logging.basicConfig(level=logging.INFO)

# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
API_TOKEN = "5606825434:AAFiDvCK1j6fJWPzReLfr990QAdO8ipY2Jc"

# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
ACCESS_ID = "581756128"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
#dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Бот обліуку витрат\n\n"
        "Добавити витрати: 250 таксі\n"
        "Статистика за поточний день: /today\n"
        "За поточний місяць: /month\n"
        "Останні внесені витрати: /expenses\n"
        "Категорії витрат: /categories")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Видаляє запис про видатки  по  ідентифікатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Видалено"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Категорії витрат:\n\n* " +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Відправляє сьогоднішню статистику витрат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Віправляє статистику витрат поточного місяця"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Відправляє останні записи  про витрати"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Витрати ще не заведені")
        return

    last_expenses_rows = [
        f"{expense.amount} грн. на {expense.category_name} — натисни "
        f"/del{expense.id} для видалення"
        for expense in last_expenses]
    answer_message = "Останні збережені витрати:\n\n* " + "\n\n* "\
            .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляє нові витрати"""
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлені витрати {expense.amount} грн на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
