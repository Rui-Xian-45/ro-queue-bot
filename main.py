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

# 👉 固定 View（避免重複 instance）
main_view = QueueView()


# =========================
# 更新畫面
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
            view=main_view   # ✅ 固定 instance
        )

    except Exception as e:
        print("⚠ update_panel error:", e)


# =========================
# STEP 2：安全 hook（修正版）
# =========================

def wrap(func):
    def sync_wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # async safe trigger
        bot.loop.create_task(update_panel())

        return result

    return sync_wrapper


# =========================
# STEP 3：掛載 QueueManager
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

    bot.add_view(main_view)  # ✅ persistent fixed view


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
        view=main_view
    )

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = ctx.channel.id
    queue.save()

    await ctx.send("✅ RO 排隊系統已建立")


# =========================
# 手動更新
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
