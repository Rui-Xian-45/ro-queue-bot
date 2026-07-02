class QueueView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # =====================
    # 加入
    # =====================
    @discord.ui.button(
        label="🟢 加入",
        style=discord.ButtonStyle.green,
        custom_id="queue_join"
    )
    async def join(self, interaction, button):

        r = queue.add_player(interaction.user.id)

        if r == "locked":
            return await interaction.response.send_message("❌ 已鎖定", ephemeral=True)
        if r == "exists":
            return await interaction.response.send_message("❌ 已在隊列", ephemeral=True)
        if r == "full":
            return await interaction.response.send_message("❌ 隊列已滿（25人）", ephemeral=True)

        await interaction.response.send_message("✅ 已加入", ephemeral=True)

    # =====================
    # 離開
    # =====================
    @discord.ui.button(
        label="🔴 離開",
        style=discord.ButtonStyle.red,
        custom_id="queue_leave"
    )
    async def leave(self, interaction, button):

        queue.remove_player(interaction.user.id)

        await interaction.response.send_message("✅ 已離開", ephemeral=True)

    # =====================
    # 下一組
    # =====================
    @discord.ui.button(
        label="▶ 下一組",
        style=discord.ButtonStyle.blurple,
        custom_id="queue_next"
    )
    async def next(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        queue.next_group()

        await interaction.response.send_message("🔔 已切換下一組", ephemeral=True)

    # =====================
    # 踢人
    # =====================
    @discord.ui.button(
        label="👢 踢人",
        style=discord.ButtonStyle.gray,
        custom_id="queue_kick"
    )
    async def kick(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        await interaction.response.send_message(
            "選擇要踢出的玩家：",
            view=KickView(),
            ephemeral=True
        )

    # =====================
    # 完成副本
    # =====================
    @discord.ui.button(
        label="🏁 完成副本",
        style=discord.ButtonStyle.green,
        custom_id="queue_finish"
    )
    async def finish(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        queue.finish_run()

        await interaction.response.send_message(
            "🏁 已完成副本（隊伍已清空）",
            ephemeral=True
        )
