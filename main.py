import discord
from discord.ext import commands
import os

from views import QueueView
from embeds import build_embed
from queue_manager import QueueManager

# =========================
# Bot 設定
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()


# =========================
# 啟動
# =========================

@bot.event
async def on_ready():
    print(f"✅ Bot 已上線：{bot.user}")

    # Persistent View（唯一）
    bot.add_view(QueueView())

    print("🔄 Views 已載入")


# =========================
# 建立主面板
# =========================

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

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

    queue.data["channel_id"] = ctx.channel.id
    queue.data["message_id"] = msg.id
    queue.save()

    await ctx.send("✅ RO 排隊系統已建立")


# =========================
# 更新面板
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
        print("⚠ 更新失敗:", e)


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
