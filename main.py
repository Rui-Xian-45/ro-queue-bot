import discord
from discord.ext import commands
import os

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
# STEP 1：更新畫面函式
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
            view=QueueView()
        )

    except Exception as e:
        print("⚠ update_panel error:", e)


# =========================
# STEP 2：Trigger 包裝器
# =========================

def wrap(func):
    async def async_wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # 自動更新 UI
        await update_panel()

        return result

    return async_wrapper


# =========================
# STEP 3：掛載 QueueManager 自動更新
# =========================

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

    # Persistent View（重啟不壞按鈕）
    bot.add_view(QueueView())


# =========================
# 建立排隊面板
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

    await ctx.send("✅ RO 排隊系統已建立")


# =========================
# 手動更新（保留備用）
# =========================

@bot.command()
async def refresh(ctx):
    await update_panel()
    await ctx.send("🔄 OK")


# =========================
# Token
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
