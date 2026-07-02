import discord
from discord import app_commands

# =========================
# HELP
# =========================
@bot.tree.command(name="help", description="顯示所有指令")
async def help_cmd(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📌 RO 排隊系統指令",
        color=discord.Color.green()
    )

    embed.add_field(
        name="🟢 玩家指令",
        value=(
            "/join 加入排隊\n"
            "/leave 離開排隊\n"
            "/status 查看狀態"
        ),
        inline=False
    )

    embed.add_field(
        name="👑 管理員",
        value=(
            "/setup 建立面板\n"
            "/kick 踢人\n"
            "/lock 鎖房\n"
            "/unlock 解鎖\n"
            "/grant 授權管理員"
        ),
        inline=False
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)


# =========================
# JOIN
# =========================
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


# =========================
# LEAVE
# =========================
@bot.tree.command(name="leave", description="離開排隊")
async def leave(interaction: discord.Interaction):

    queue.remove_player(interaction.user.id)

    await interaction.response.send_message("✅ 已離開", ephemeral=True)


# =========================
# STATUS
# =========================
@bot.tree.command(name="status", description="查看排隊狀態")
async def status(interaction: discord.Interaction):

    members = queue.data["members"]
    current = queue.get_current_group()

    await interaction.response.send_message(
        f"👥 人數：{len(members)}/25\n"
        f"🎮 副本中：{current}",
        ephemeral=True
    )


# =========================
# SETUP（管理員）
# =========================
@bot.tree.command(name="setup", description="建立排隊面板")
@app_commands.checks.has_permissions(administrator=True)
async def setup(interaction: discord.Interaction):

    msg = await interaction.channel.send(
        embed=build_embed(queue),
        view=queue_view
    )

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = interaction.channel.id

    await interaction.response.send_message("✅ 面板已建立", ephemeral=True)


# =========================
# KICK（管理員）
# =========================
@bot.tree.command(name="kick", description="踢人")
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: discord.Interaction, user: discord.Member):

    queue.kick_player(user.id)

    await interaction.response.send_message(f"👢 已踢出 {user.display_name}", ephemeral=True)


# =========================
# LOCK
# =========================
@bot.tree.command(name="lock", description="鎖房")
@app_commands.checks.has_permissions(administrator=True)
async def lock(interaction: discord.Interaction):

    queue.lock()
    await interaction.response.send_message("🔒 已鎖房", ephemeral=True)


# =========================
# UNLOCK
# =========================
@bot.tree.command(name="unlock", description="解鎖房間")
@app_commands.checks.has_permissions(administrator=True)
async def unlock(interaction: discord.Interaction):

    queue.unlock()
    await interaction.response.send_message("🔓 已解鎖", ephemeral=True)


# =========================
# GRANT ADMIN
# =========================
@bot.tree.command(name="grant", description="授權房間管理員")
@app_commands.checks.has_permissions(administrator=True)
async def grant(interaction: discord.Interaction, user: discord.Member):

    queue.add_room_admin(user.id)

    await interaction.response.send_message(
        f"👑 已授權 {user.display_name}",
        ephemeral=True
    )
