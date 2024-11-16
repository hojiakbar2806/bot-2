import aiohttp
import requests

from aiogram.types import Message


async def check_qiwi_token(token: str):
    if token is not None:
        headers = dict(
            Accept='application/json',
            Authorization='Bearer ' + token
        )
        headers['Content-Type'] = 'application/json'
        url = 'https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true'

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, headers=headers) as resp:
                try:
                    resp_json = await resp.json()

                    if resp_json.get("errorCode", False) is not False:
                        return None
                    else:
                        return True if resp_json['contractInfo']['blocked'] == "True" else False
                except Exception as e:
                    print(e)
                    return None
    else:
        return None


def create_payment_url(message, settings: dict, comment: str, amount: int | float):
    text = "<b>Никнейм: </b>" + f"<code>{message.bot.config.payments.qiwi.qiwi_api.nick}</code>" \
        if settings['nickname'] is True \
        else f"<b>Номер телефона: </b>" + f"<code>{message.bot.config.payments.qiwi.qiwi_api.phone}</code>"

    if settings['nickname'] is False:
        url = f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={message.bot.config.payments.qiwi.qiwi_api.phone}&amountInteger={amount}&amountFraction=0&extra%5B%27comment%27%5D={comment}&currency=643&blocked%5B0%5D=sum&blocked%5B1%5D=comment&blocked%5B2%5D=account"
    else:
        url = f"https://qiwi.com/payment/form/99999?amountInteger={amount}&amountFraction=0&currency=643&extra%5B%27comment%27%5D={comment}&extra%5B%27account%27%5D={message.bot.config.payments.qiwi.qiwi_api.nick}&blocked%5B0%5D=comment&blocked%5B1%5D=account&blocked%5B2%5D=sum&0%5Bextra%5B%27accountType%27%5D%5D=nickname"

    text += "\n\n"
    return text, url


async def payment_history_last(my_login: str, api_access_token: str,
                               rows_num: int = 20):
    #headers = dict(authorization='Bearer ' + api_access_token)
    headers = {"authorization": f"Bearer {api_access_token}"}
    params = dict(rows=rows_num, operation="IN")
    url = 'https://edge.qiwi.com/payment-history/v2/persons/' + my_login[1:] + '/payments'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            try:
                print(await response.read())
                return await response.json()
            except Exception as e:
                print(e)
                return None
