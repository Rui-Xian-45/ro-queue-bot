import discord
from discord.ext import commands
from discord import app_commands
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

# ⭐ 全域單一 View（重要：避免炸 persistent view）
queue_view = QueueView()


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
            view=queue_view   # ⭐ 固定 instance
        )

    except Exception as e:
        print("⚠ update_panel error:", e)


# =========================
# AUTO UPDATE HOOK
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
queue.clear = wrap(queue.clear)
queue.lock = wrap(queue.lock)
queue.unlock = wrap(queue.unlock)


# =========================
# Slash /help
# =========================

@bot.tree.command(name="help", description="顯示所有 RO 排隊指令")
async def help_cmd(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📌 RO 排隊系統",
        color=discord.Color.green()
    )

    embed.add_field(
        name="🏠 基本操作",
        value=(
            "🟢 加入：加入排隊\n"
            "🔴 離開：退出排隊\n"
            "🏁 完成副本：推進 3 人"
        ),
        inline=False
    )

    embed.add_field(
        name="👑 管理員",
        value=(
            "!setup 建立排隊面板\n"
            "踢人 / 鎖房（管理功能）"
        ),
        inline=False
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)


# =========================
# Bot 啟動
# =========================

@bot.event
async def on_ready():
    print(f"✅ {bot.user}")

    # ⭐ Persistent View（只註冊一次）
    bot.add_view(queue_view)

    # ⭐ Slash 同步（關鍵）
    try:
        await bot.tree.sync()
        print("✅ Slash commands synced")
    except Exception as e:
        print("⚠ sync error:", e)


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
        view=queue_view
    )

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = ctx.channel.id
    queue.save()

    await ctx.send("✅ 排隊系統完成")


# =========================
# Token
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN 沒有設定（請檢查 Railway Variables）")

bot.run(TOKEN)
