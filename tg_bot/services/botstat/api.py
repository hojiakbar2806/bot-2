import aiobotstat
import aiobotstat.const


class BotStats(aiobotstat.BotStatAPI):
    async def __aenter__(self) -> aiobotstat.BotStatAPI:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def send_to_botman(self, bot_token: str, owner_id: int, file):
        """Result of checks."""
        method = aiobotstat.const.HTTPMethods.POST
        url = f"{self.BASE_URL}/botman/{bot_token}?owner_id={owner_id}"

        data = await self._make_request(method, url, data={"file": file})
        return data.json()
