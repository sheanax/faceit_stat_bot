import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from faceit import get_player, get_stats

router = Router()
FACEIT_API_KEY = os.getenv("FACEIT_API_KEY")

@router.message(Command("stats"))
async def stats_handler(message: Message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Укажи ник игрока: /stats s1mple")
        return
    nickname = parts[1]
    await message.answer("Ищу.........")
    player = await get_player(FACEIT_API_KEY, nickname)
    if not player:
        await message.answer(f"Игрок {nickname} не найден на Faceit")
        return
    if "cs2" not in player.get("games", {}):
        await message.answer(f"У игрока {nickname} нет статистики по CS2 на Faceit")
        return
    player_id = player["player_id"]
    elo = player["games"]["cs2"]["faceit_elo"]
    level = player["games"]["cs2"]["skill_level"]
    stats = await get_stats(FACEIT_API_KEY, player_id)
    if not stats:
        await message.answer(f"Не удалось получить статистику")
        return
    lifetime = stats["lifetime"]
    text = (
        f"Игрок: {player['nickname']}\n"
        f"Уровень: {level} ({elo} ELO)\n"
        f"Матчей сыграно: {lifetime['Matches']}\n"
        f"K/D: {lifetime['Average K/D Ratio']}\n"
        f"Винрейт: {lifetime['Win Rate %']}%\n"
        f"Хедшоты: {lifetime['Average Headshots %']}%"
    )
    await message.answer(text)