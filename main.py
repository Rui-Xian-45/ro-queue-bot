import discord
from discord.ext import commands
import os
import asyncio

from queue_manager import QueueManager
from views import QueueView
from embeds import build_embed


# =====================
# BOT INIT
# =====================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()
queue_view = None


# =====================
# READY
# =====================
@bot.event
async def on_ready():
    global queue_view

    print(f"✅ Logged in as {bot.user}")

    queue_view = QueueView(queue)

    bot.add_view(queue_view)

    try:
        await bot.tree.sync()
        print("✅ Slash commands synced")
    except Exception as e:
        print("❌ sync error:", e)


# =====================
# UI UPDATE
# =====================
async def update_panel():

    if not queue.data["message_id"]:
        return

    channel = bot.get_channel(queue.data["channel_id"])
    if not channel:
        return

    try:
        msg = await channel.fetch_message(queue.data["message_id"])

        guild = channel.guild

        await msg.edit(
            embed=build_embed(queue, guild),
            view=queue_view
        )

    except Exception as e:
        print("update error:", e)


# =====================
# AUTO WRAPPER
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
queue.kick_player = wrap(queue.kick_player)


# =====================
# HELP
# =====================
@bot.tree.command(name="help", description="顯示所有指令")
async def help_cmd(interaction: discord.Interaction):

    await interaction.response.send_message(
        "🟢 /join 加入\n🔴 /leave 離開\n🏁 /finish 副本\n👢 /kick 踢人",
        ephemeral=True
    )


# =====================
# JOIN
# =====================
@bot.tree.command(name="join", description="加入排隊")
async def join(interaction: discord.Interaction):

    r = queue.add_player(interaction.user.id)

    if r == "full":
        return await interaction.response.send_message("❌ 滿了", ephemeral=True)
    if r == "exists":
        return await interaction.response.send_message("❌ 已在隊伍", ephemeral=True)
    if r == "locked":
        return await interaction.response.send_message("❌ 已鎖房", ephemeral=True)

    await interaction.response.send_message("✅ 已加入", ephemeral=True)


# =====================
# LEAVE
# =====================
@bot.tree.command(name="leave", description="離開排隊")
async def leave(interaction: discord.Interaction):

    queue.remove_player(interaction.user.id)
    await interaction.response.send_message("✅ 已離開", ephemeral=True)


# =====================
# FINISH（🔥 已修正核心）
# =====================
@bot.tree.command(name="finish", description="完成副本（推進3人）")
async def finish(interaction: discord.Interaction):

    if not (
        interaction.user.guild_permissions.administrator
    ):
        return await interaction.response.send_message("❌ 無權限", ephemeral=True)

    members = queue.data["members"]
    i = queue.data["current_index"]

    current = members[i:i+3]
    next_group = members[i+3:i+6]

    # 👉 推進
    queue.finish_run()

    # =====================
    # 下一組通知
    # =====================
    if next_group:
        mentions = " ".join([f"<@{uid}>" for uid in next_group])

        await interaction.channel.send(
            f"🔥 下一組進副本：{mentions}"
        )
    else:
        await interaction.channel.send("🏁 已無下一組，副本結束")

    await interaction.response.send_message(
        "✅ 副本已完成",
        ephemeral=True
    )


# =====================
# KICK
# =====================
@bot.tree.command(name="kick", description="踢人")
async def kick(interaction: discord.Interaction, user: discord.Member):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ 無權限", ephemeral=True)

    queue.kick_player(user.id)
    await interaction.response.send_message(
        f"👢 已踢 {user.display_name}",
        ephemeral=True
    )


# =====================
# SETUP
# =====================
@bot.tree.command(name="setup", description="建立排隊面板")
async def setup(interaction: discord.Interaction):

    msg = await interaction.channel.send(
        embed=build_embed(queue, interaction.guild),
        view=queue_view
    )

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = interaction.channel.id

    await interaction.response.send_message("✅ 已建立面板", ephemeral=True)


# =====================
# RUN
# =====================
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN 沒設定")

bot.run(TOKEN)
