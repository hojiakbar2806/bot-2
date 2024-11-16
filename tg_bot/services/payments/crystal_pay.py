import aiohttp

from json import dumps


API_URL = "https://api.crystalpay.io/v2/{}/{}/"


class AuthError(Exception):
    pass


class CreatePaymentError(Exception):
    pass


class CheckPaymentErr(Exception):
    pass


class Payment:
    def __init__(self, payment_id: str, default_params: dict, amount: int = None):
        self.id = payment_id
        self.default_params = default_params
        self.url = f"https://pay.crystalpay.io/?i={self.id}"
        self.api_url = API_URL.format("invoice", "info")
        self.headers = {'Content-Type': 'application/json'}
        self.amount = amount

        self.request_json_data = dumps(dict(auth_login=self.default_params["auth_login"],
                                            auth_secret=self.default_params["auth_secret"],
                                            id=self.id))

    async def send_request(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.api_url, data=self.request_json_data) as response:
                result = await response.json()

            if result.get("error", False) is True:
                raise Exception(f"Ошибка: {result['error']}")

        return result

    async def check_paid(self) -> bool:
        result = await self.send_request()
        if result['state'] == "payed":
            return True

    async def get_amount(self) -> None:
        result = await self.send_request()
        return result['amount']


class CrystalPay:
    def __init__(self, cash_name: str, secret_1: str):
        """
        cash_name - имя кассы/логин
        secret_1 - секретный ключ 1
        """
        self.login = cash_name
        self.secret_key = secret_1
        self.api_url = API_URL.format("invoice", "create")
        self.default_params = dict(auth_login=self.login, auth_secret=self.secret_key,
                                   type='purchase', lifetime=10)
        self.headers = {'Content-Type': 'application/json'}
        self.session = aiohttp.ClientSession()

    async def send_request(self, url, headers, json_data):
        try:
            async with self.session.post(url, headers=headers, json=json_data) as response:
                result = await response.json()

                if result.get("error", False) is True:
                    await self.session.close()
                    raise Exception(''.join(result['errors']))

            return result
        except Exception as e:
            await self.session.close()
            raise Exception(f"Ошибка: {e}")

    async def get_me(self):
        url = API_URL.format("me", "info")

        result = await self.send_request(url, self.headers, self.default_params)
        try:
            return result["name"]
        except:
            raise AuthError("Проверьте токен/соль.")

    async def create_invoice(self, amount: int, invoice_type: str = None, currency: str = None,
                       lifetime: int = None, redirect_url: str = None,
                       callback: str = None, extra: str = None,
                       payment_system: str = None) -> Payment:

        temp_params = self.default_params
        temp_params['amount'] = amount

        if currency:
            temp_params['currency'] = currency
        if invoice_type:
            temp_params['type'] = invoice_type
        if lifetime:
            temp_params['lifetime'] = lifetime
        if redirect_url:
            temp_params['redirect_url'] = redirect_url
        if callback:
            temp_params['callback'] = callback
        if extra:
            temp_params['extra'] = extra
        if payment_system:
            temp_params['m'] = payment_system

        result = await self.send_request(self.api_url, self.headers, temp_params)

        try:
            return Payment(result['id'], self.default_params, amount)
        except:
            raise CreatePaymentError("Введенные данные неправильны.")

    def construct_payment_by_id(self, payment_id) -> Payment:
        return Payment(payment_id, self.default_params)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def __aenter__(self):
        self.user = await self.get_me()
        return self
