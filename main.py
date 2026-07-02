import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio

from views import QueueView
from embeds import build_embed
from queue_manager import QueueManager


# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()
queue_view = QueueView(queue)


# =========================
# 啟動自動建房（單一房間）
# =========================

@bot.event
async def on_ready():
    print(f"✅ {bot.user}")

    # ⭐ 自動建立單一房間（只做一次）
    if not queue.data.get("room_created"):
        queue.create_room(owner_id=None)  # 無特定房主（全服房）
        queue.data["room_created"] = True

    # ⭐ persistent view
    bot.add_view(queue_view)

    # ⭐ slash sync
    try:
        await bot.tree.sync()
        print("✅ Slash synced")
    except Exception as e:
        print("⚠ sync error:", e)


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
            embed=build_embed(queue),
            view=queue_view
        )

    except Exception as e:
        print("⚠ update_panel error:", e)


# =========================
# HOOK（自動更新 UI）
# =========================

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
queue.next_group = wrap(queue.next_group)
queue.finish_run = wrap(queue.finish_run)
queue.kick_player = wrap(queue.kick_player)


# =========================
# /HELP
# =========================

@bot.tree.command(name="help", description="顯示所有指令")
async def help_cmd(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📌 RO 副本排隊系統",
        color=discord.Color.green()
    )

    embed.add_field(
        name="🎮 玩家指令",
        value=(
            "🟢 加入排隊\n"
            "🔴 退出排隊\n"
        ),
        inline=False
    )

    embed.add_field(
        name="⚔ 副本系統",
        value=(
            "🏁 完成副本（每次 3 人）\n"
            "顯示：副本中 / 排隊中 / 完成"
        ),
        inline=False
    )

    embed.add_field(
        name="👑 管理員",
        value=(
            "踢人 / 鎖房 / 授權管理員\n"
            "!setup 建立面板"
        ),
        inline=False
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)


# =========================
# 建立面板
# =========================

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    msg = await ctx.send(
        embed=build_embed(queue),
        view=queue_view
    )

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = ctx.channel.id

    await ctx.send("✅ RO 排隊系統已啟動")


# =========================
# TOKEN
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN 沒設定")

bot.run(TOKEN)
