import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio

from queue_manager import QueueManager
from views import QueueView
from embeds import build_embed


# =====================
# BOT SETUP
# =====================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()

# ⚠️ 不要在這裡建立 View（會炸）
queue_view = None


# =====================
# READY EVENT
# =====================

@bot.event
async def on_ready():
    global queue_view

    print(f"✅ {bot.user}")

    # ⭐ 這裡才建立 View（關鍵修正）
    queue_view = QueueView(queue)

    bot.add_view(queue_view)

    await bot.tree.sync()
    print("✅ Slash synced")


# =====================
# UI 更新
# =====================

async def update_panel():

    if not queue.data["message_id"]:
        return

    channel = bot.get_channel(queue.data["channel_id"])
    if not channel:
        return

    try:
        msg = await channel.fetch_message(queue.data["message_id"])

        await msg.edit(
            embed=build_embed(queue),
            view=queue_view
        )

    except Exception as e:
        print("⚠ update_panel error:", e)


# =====================
# AUTO UPDATE HOOK
# =====================

def wrap(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)

        try:
            asyncio.get_running_loop().create_task(update_panel())
        except RuntimeError:
            pass

        return result
    return inner


queue.add_player = wrap(queue.add_player)
queue.remove_player = wrap(queue.remove_player)
queue.finish_run = wrap(queue.finish_run)


# =====================
# HELP
# =====================

@bot.tree.command(name="help")
async def help_cmd(interaction: discord.Interaction):

    await interaction.response.send_message(
        "🟢 加入 / 🔴 離開 / 🏁 完成副本 / 👢 踢人",
        ephemeral=True
    )


# =====================
# SETUP
# =====================

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    msg = await ctx.send(
        embed=build_embed(queue),
        view=queue_view
    )

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = ctx.channel.id

    await ctx.send("✅ 已建立排隊系統")


# =====================
# TOKEN
# =====================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN 沒設定")

bot.run(TOKEN)
