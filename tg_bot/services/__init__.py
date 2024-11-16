from aiogram import Dispatcher


async def notify_payment_to_owner(
        dp: Dispatcher, service_name: str,
        amount: int | float, user_id: int | str):
    text = f'<b>♻️ Пришло пополнение</b> <code>{service_name}</code>\n'\
           f'<b>🧑🏻‍🔧 От:</b> <code>{user_id}</code>\n'\
           f'<b>💰 Сумма:</b> <code>{amount} ₽</code>'

    await dp.bot.send_message(dp.bot.config.owner_id, text)


async def notify_error_to_owner(
        dp: Dispatcher, service_name: str, exception_text):
    text = f'<b>❌ Не работает пополнение через {service_name}</b>\n\n' \
           f'<code>{exception_text}</code>'\

    await dp.bot.send_message(dp.bot.config.owner_id, text)
