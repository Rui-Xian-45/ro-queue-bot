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
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()

# 記錄主面板
panel_message_id = None
panel_channel_id = None


# =========================
# 啟動
# =========================

@bot.event
async def on_ready():
    print(f"✅ Bot 已上線：{bot.user}")

    # Persistent View（重啟不壞按鈕）
    bot.add_view(QueueView())

    print("🔄 Views 已載入")


# =========================
# 建立主面板
# =========================

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    global panel_message_id, panel_channel_id

    # 防止重複建立
    if queue.data["message_id"]:
        await ctx.send("⚠ 已經建立過排隊面板了")
        return

    embed = build_embed()

    view = QueueView()

    msg = await ctx.send(
        embed=embed,
        view=view
    )

    panel_message_id = msg.id
    panel_channel_id = ctx.channel.id

    queue.data["message_id"] = panel_message_id
    queue.data["channel_id"] = panel_channel_id
    queue.save()

    await ctx.send("✅ RO 排隊系統已建立完成")


# =========================
# 🔄 更新主面板（核心）
# =========================

async def update_panel():

    if not queue.data["channel_id"] or not queue.data["message_id"]:
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
        print("更新失敗:", e)


# =========================
# ⚡ 自動更新 Hook（關鍵）
# =========================

# Monkey patch queue_manager（讓按鈕操作後會更新 UI）

original_add = queue.add_player
original_remove = queue.remove_player
original_next = queue.next_group
original_clear = queue.clear
original_lock = queue.lock
original_unlock = queue.unlock


def wrap(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        bot.loop.create_task(update_panel())
        return result
    return inner


queue.add_player = wrap(original_add)
queue.remove_player = wrap(original_remove)
queue.next_group = wrap(original_next)
queue.clear = wrap(original_clear)
queue.lock = wrap(original_lock)
queue.unlock = wrap(original_unlock)


# =========================
# 手動更新
# =========================

@bot.command()
@commands.has_permissions(administrator=True)
async def refresh(ctx):
    await update_panel()
    await ctx.send("🔄 已更新排隊面板")


# =========================
# Token
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)
