import aiohttp

BASE_URL = "https://open.faceit.com/data/v4"

async def get_player(api_key: str, nickname: str) -> dict | None:
    # говорим серверу кто мы — передаём ключ
    headers = {"Authorization": f"Bearer {api_key}"}
    
    async with aiohttp.ClientSession(headers=headers) as session:
        # делаем запрос, nickname передаём как ?nickname=s1mple в урле
        async with session.get(f"{BASE_URL}/players", params={"nickname": nickname}) as resp:
            # такого игрока нет — возвращаем None
            if resp.status == 404:
                return None
            
            # всё ок — превращаем ответ в словарь и отдаём
            data = await resp.json()
            return data


async def get_stats(api_key: str, player_id: str) -> dict | None:
    headers = {"Authorization": f"Bearer {api_key}"}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{BASE_URL}/players/{player_id}/games/cs2") as resp:
            if resp.status == 404:
                return None
            
            data = await resp.json()
            return data