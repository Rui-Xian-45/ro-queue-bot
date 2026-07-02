import discord


class QueueView(discord.ui.View):
    def __init__(self, queue):
        super().__init__(timeout=None)
        self.queue = queue

    @discord.ui.button(label="加入", style=discord.ButtonStyle.green)
    async def join(self, interaction, button):

        r = self.queue.add_player(interaction.user.id)

        if r == "full":
            return await interaction.response.send_message("❌ 滿了", ephemeral=True)

        if r == "exists":
            return await interaction.response.send_message("❌ 已在隊伍", ephemeral=True)

        if r == "locked":
            return await interaction.response.send_message("❌ 已鎖房", ephemeral=True)

        await interaction.response.send_message("✅ 已加入", ephemeral=True)


    @discord.ui.button(label="離開", style=discord.ButtonStyle.red)
    async def leave(self, interaction, button):

        self.queue.remove_player(interaction.user.id)
        await interaction.response.send_message("✅ 已離開", ephemeral=True)


    @discord.ui.button(label="完成副本", style=discord.ButtonStyle.blurple)
    async def finish(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        self.queue.finish_run()
        await interaction.response.send_message("🏁 已推進", ephemeral=True)
