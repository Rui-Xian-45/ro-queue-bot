import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio

from queue_manager import QueueManager
from views import QueueView
from embeds import build_embed


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()
queue_view = QueueView(queue)


# =====================
# update UI
# =====================
async def update_panel():

    if not queue.data["message_id"]:
        return

    channel = bot.get_channel(queue.data["channel_id"])
    if not channel:
        return

    try:
        msg = await channel.fetch_message(queue.data["message_id"])
        await msg.edit(embed=build_embed(queue), view=queue_view)
    except:
        pass


# =====================
# auto update
# =====================
def wrap(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            asyncio.get_running_loop().create_task(update_panel())
        except:
            pass
        return result
    return inner


queue.add_player = wrap(queue.add_player)
queue.remove_player = wrap(queue.remove_player)
queue.finish_run = wrap(queue.finish_run)


# =====================
# /help
# =====================
@bot.tree.command(name="help")
async def help_cmd(interaction: discord.Interaction):

    await interaction.response.send_message(
        "🟢 加入 / 🔴 離開 / 完成副本 / 踢人",
        ephemeral=True
    )


# =====================
# setup
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
# ready
# =====================
@bot.event
async def on_ready():
    print(f"✅ {bot.user}")

    bot.add_view(queue_view)

    await bot.tree.sync()


# =====================
# token
# =====================
TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)
