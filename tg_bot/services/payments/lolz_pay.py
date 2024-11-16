import asyncio
import aiohttp


class Lolz:
    def __init__(self, access_token: str):
        self.api_url = 'https://api.zelenka.guru/'

        self.headers = dict(Authorization="Bearer " + access_token)
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def send_request(self, url, headers=None):
        try:
            async with self.session.get(url, headers=headers) as response:
                result = await response.json()
                return result
        except Exception as e:
            await self.session.close()
            _text = await response.text()
            raise BaseException(_text.split('<h1>')[1].split('</h1>')[0])

    async def get_user(self):
        result = await self.send_request('https://api.lzt.market/me', headers=self.headers)
        if 'user' not in result.keys():
            raise ValueError('Invalid Token')
        return result['user']

    async def get_link(self, amount: int | float, comment: str, hold: int):
        return f'https://lzt.market/balance/transfer?username={self.user["username"]}&hold={hold}&amount={amount}&comment={comment}'

    async def check_payment(self, comment: str):
        result = await self.send_request(f'{self.api_url}market/user/{self.user["user_id"]}/payments')
        payments = result['payments']
        for payment in payments.values():
            if 'Перевод денег от' in payment['label']['title'] and comment == payment['data']['comment']:
                return payment
        return False

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def __aenter__(self):
        self.user = await self.get_user()
        return self
