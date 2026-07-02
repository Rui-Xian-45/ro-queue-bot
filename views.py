import discord

class QueueView(discord.ui.View):
    def __init__(self, queue):
        super().__init__(timeout=None)
        self.queue = queue

    # =====================
    # 加入
    # =====================
    @discord.ui.button(label="加入", style=discord.ButtonStyle.green, custom_id="join")
    async def join(self, interaction, button):

        r = self.queue.add_player(interaction.user.id)

        if r == "full":
            return await interaction.response.send_message("❌ 滿了", ephemeral=True)
        if r == "exists":
            return await interaction.response.send_message("❌ 已在隊伍", ephemeral=True)
        if r == "locked":
            return await interaction.response.send_message("❌ 已鎖房", ephemeral=True)

        await interaction.response.send_message("✅ 已加入", ephemeral=True)

    # =====================
    # 離開
    # =====================
    @discord.ui.button(label="離開", style=discord.ButtonStyle.red, custom_id="leave")
    async def leave(self, interaction, button):

        self.queue.remove_player(interaction.user.id)
        await interaction.response.send_message("✅ 已離開", ephemeral=True)

    # =====================
    # 完成副本
    # =====================
    @discord.ui.button(label="完成副本", style=discord.ButtonStyle.blurple, custom_id="finish")
    async def finish(self, interaction, button):

        if not (
            interaction.user.guild_permissions.administrator or
            self.queue.is_admin(interaction.user.id)
        ):
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        self.queue.finish_run()

        await interaction.response.send_message("🏁 已推進 3 人", ephemeral=True)

    # =====================
    # 踢人（簡化）
    # =====================
    @discord.ui.button(label="踢人", style=discord.ButtonStyle.gray, custom_id="kick")
    async def kick(self, interaction, button):

        if not (
            interaction.user.guild_permissions.administrator or
            self.queue.is_admin(interaction.user.id)
        ):
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        await interaction.response.send_message("請使用指令踢人（後續可升級 UI）", ephemeral=True)
