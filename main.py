import discord
from discord.ext import commands
import os
import asyncio

from views import QueueView
from embeds import build_embed
from queue_manager import QueueManager


# =========================
# Bot 基本設定
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()


# =========================
# UI 更新
# =========================

async def update_panel():

    if not queue.data["message_id"]:
        return

    channel = bot.get_channel(queue.data["channel_id"])
    if not channel:
        return

    try:
        msg = await channel.fetch_message(queue.data["message_id"])

        await msg.edit(
            embed=build_embed(),
            view=QueueView()   # ✅ 每次重新建立（安全）
        )

    except Exception as e:
        print("⚠ update_panel error:", e)


# =========================
# AUTO UPDATE HOOK（安全版）
# =========================

def wrap(func):

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)

        # ⚠ 避免 loop not ready crash
        try:
            asyncio.get_running_loop().create_task(update_panel())
        except RuntimeError:
            pass

        return result

    return inner


queue.add_player = wrap(queue.add_player)
queue.remove_player = wrap(queue.remove_player)
queue.next_group = wrap(queue.next_group)
queue.clear = wrap(queue.clear)
queue.lock = wrap(queue.lock)
queue.unlock = wrap(queue.unlock)


# =========================
# Bot 啟動
# =========================

@bot.event
async def on_ready():
    print(f"✅ {bot.user}")

    # ✅ Persistent Views（正確位置）
    bot.add_view(QueueView())


# =========================
# 建立面板
# =========================

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    if queue.data["message_id"]:
        return await ctx.send("⚠ 已建立")

    msg = await ctx.send(
        embed=build_embed(),
        view=QueueView()
    )

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = ctx.channel.id
    queue.save()

    await ctx.send("✅ V1.2 排隊系統完成")


# =========================
# Token
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
