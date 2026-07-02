import discord
from discord.ext import commands

from views import PlayerView, AdminView
from embeds import build_embed
from queue_manager import QueueManager

import os

# =========================
# Bot 設定
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()

CHANNEL_ID = None
MESSAGE_ID = None


# =========================
# Bot 啟動
# =========================

@bot.event
async def on_ready():
    print(f"✅ Bot 已上線：{bot.user}")

    # 恢復 persistent views
    bot.add_view(PlayerView())
    bot.add_view(AdminView())

    print("🔄 Views 已載入")


# =========================
# 發送排隊面板
# =========================

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    """
    建立排隊主面板（只需要執行一次）
    """

    global CHANNEL_ID, MESSAGE_ID

    embed = build_embed()

    view = discord.ui.View()
    view.add_item(PlayerView().children[0])
    view.add_item(PlayerView().children[1])

    # 先建立玩家 + 管理員 view
    player_view = PlayerView()
    admin_view = AdminView()

    msg = await ctx.send(
        embed=embed,
        view=player_view
    )

    # 存 ID
    CHANNEL_ID = ctx.channel.id
    MESSAGE_ID = msg.id

    queue.data["channel_id"] = CHANNEL_ID
    queue.data["message_id"] = MESSAGE_ID
    queue.save()

    await ctx.send("✅ RO 排隊系統已建立")


# =========================
# 更新畫面
# =========================

async def update_panel():
    """
    更新主面板
    """

    if not queue.data["channel_id"] or not queue.data["message_id"]:
        return

    channel = bot.get_channel(queue.data["channel_id"])
    if not channel:
        return

    try:
        msg = await channel.fetch_message(queue.data["message_id"])

        await msg.edit(
            embed=build_embed(),
            view=PlayerView()
        )

    except:
        print("⚠ 更新面板失敗")


# =========================
# 指令：手動更新
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
