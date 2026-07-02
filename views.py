import discord
from queue_manager import QueueManager
from embeds import build_embed

queue = QueueManager()


class QueueView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🟢 加入", style=discord.ButtonStyle.green, custom_id="join")
    async def join(self, interaction, button):

        r = queue.add_player(interaction.user.display_name)

        if r == "locked":
            return await interaction.response.send_message("❌ 已鎖定", ephemeral=True)
        if r == "exists":
            return await interaction.response.send_message("❌ 已在隊列", ephemeral=True)
        if r == "full":
            return await interaction.response.send_message("❌ 滿了", ephemeral=True)

        await interaction.response.send_message("✅ 已加入", ephemeral=True)

    @discord.ui.button(label="🔴 離開", style=discord.ButtonStyle.red, custom_id="leave")
    async def leave(self, interaction, button):

        ok = queue.remove_player(interaction.user.display_name)

        if ok:
            await interaction.response.send_message("✅ 已離開", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 不在隊列", ephemeral=True)

    @discord.ui.button(label="▶ 下一組", style=discord.ButtonStyle.blurple, custom_id="next")
    async def next(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        players = queue.next_group()

        if not players:
            return await interaction.response.send_message("⚠ 無人", ephemeral=True)

        await interaction.response.send_message(
            "🔔 下一組：" + " ".join(players),
            allowed_mentions=discord.AllowedMentions(users=True)
        )

    @discord.ui.button(label="🔒 鎖定", style=discord.ButtonStyle.gray, custom_id="lock")
    async def lock(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        queue.lock()
        await interaction.response.send_message("🔒 已鎖定", ephemeral=True)

    @discord.ui.button(label="🔓 開放", style=discord.ButtonStyle.gray, custom_id="unlock")
    async def unlock(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        queue.unlock()
        await interaction.response.send_message("🔓 已開放", ephemeral=True)

    @discord.ui.button(label="🗑 清空", style=discord.ButtonStyle.red, custom_id="clear")
    async def clear(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        queue.clear()
        await interaction.response.send_message("🗑 已清空", ephemeral=True)


def get_persistent_views():
    return [QueueView()]
