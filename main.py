import discord
from discord.ext import commands
import os

from views import QueueView
from embeds import build_embed
from queue_manager import QueueManager

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()

main_view = QueueView()


# =========================
# UI 更新
# =========================

async def update_panel():

    if not queue.data["message_id"]:
        return

    channel = bot.get_channel(queue.data["channel_id"])
    if not channel:
        return

    msg = await channel.fetch_message(queue.data["message_id"])

    await msg.edit(
        embed=build_embed(),
        view=main_view
    )


# =========================
# AUTO UPDATE HOOK（V1.2核心）
# =========================

def wrap(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)

        bot.loop.create_task(update_panel())

        return result

    return inner


queue.add_player = wrap(queue.add_player)
queue.remove_player = wrap(queue.remove_player)
queue.next_group = wrap(queue.next_group)
queue.clear = wrap(queue.clear)
queue.lock = wrap(queue.lock)
queue.unlock = wrap(queue.unlock)


# =========================
# Bot
# =========================

@bot.event
async def on_ready():
    print(f"✅ {bot.user}")

    bot.add_view(main_view)


@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    if queue.data["message_id"]:
        return await ctx.send("⚠ 已建立")

    msg = await ctx.send(embed=build_embed(), view=main_view)

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = ctx.channel.id
    queue.save()

    await ctx.send("✅ V1.2 排隊系統完成")


TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
