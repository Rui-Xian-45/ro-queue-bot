import discord
from queue_manager import QueueManager

queue = QueueManager()


class QueueView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # =========================
    # 加入
    # =========================
    @discord.ui.button(label="🟢 加入", style=discord.ButtonStyle.green)
    async def join(self, interaction, button):

        r = queue.add_player(interaction.user.id)

        if r == "locked":
            return await interaction.response.send_message("❌ 已鎖定", ephemeral=True)
        if r == "exists":
            return await interaction.response.send_message("❌ 已在隊列", ephemeral=True)
        if r == "full":
            return await interaction.response.send_message("❌ 已滿 60 人", ephemeral=True)

        await interaction.response.send_message("✅ 已加入", ephemeral=True)

    # =========================
    # 離開
    # =========================
    @discord.ui.button(label="🔴 離開", style=discord.ButtonStyle.red)
    async def leave(self, interaction, button):

        ok = queue.remove_player(interaction.user.id)

        if ok:
            await interaction.response.send_message("✅ 已離開", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 不在隊列", ephemeral=True)

    # =========================
    # 下一組
    # =========================
    @discord.ui.button(label="▶ 下一組", style=discord.ButtonStyle.blurple)
    async def next(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        players = queue.next_group()

        await interaction.response.send_message(
            f"🔔 下一組：{len(players)} 人",
            ephemeral=True
        )

    # =========================
    # 踢人（新增🔥）
    # =========================
    @discord.ui.button(label="👢 踢人", style=discord.ButtonStyle.gray)
    async def kick(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        await interaction.response.send_message(
            "請輸入要踢出的 Discord ID",
            ephemeral=True
        )

        def check(msg):
            return msg.author == interaction.user

        msg = await interaction.client.wait_for("message", check=check)

        try:
            user_id = int(msg.content)
        except:
            return await msg.reply("❌ ID 錯誤")

        ok = queue.kick_player(user_id)

        if ok:
            await msg.reply("✅ 已踢出")
        else:
            await msg.reply("❌ 找不到該玩家")
