# =====================
# FINISH
# =====================
@bot.tree.command(name="finish", description="完成副本")
async def finish(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ 無權限",
            ephemeral=True
        )

    # 取得目前下一組（完成後會變成副本中）
    next_group = queue.data["members"][3:6]

    # 移除副本中的前三位
    queue.finish_run()

    # 更新畫面
    await update_panel()

    # 通知下一組
    if next_group:
        names = []

        for uid in next_group:
            member = interaction.guild.get_member(uid)
            if member:
                names.append(member.display_name)

        if names:
            await interaction.channel.send(
                f"🔥 下一組請進副本：\n" + "\n".join(names)
            )
    else:
        await interaction.channel.send("🏁 已無下一組")

    await interaction.response.send_message(
        "✅ 已完成副本",
        ephemeral=True
    )
