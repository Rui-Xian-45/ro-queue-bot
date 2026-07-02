import discord
from queue_manager import QueueManager

queue = QueueManager()


# =========================
# Kick 選單（動態版本）
# =========================

class KickSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(
            placeholder="選擇要踢出的玩家",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 沒權限", ephemeral=True)

        user_id = int(self.values[0])

        ok = queue.kick_player(user_id)

        if ok:
            await interaction.response.send_message("✅ 已踢出", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 找不到玩家", ephemeral=True)


class KickView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

        # 🔥 每次開啟都重新生成（關鍵修正）
        options = [
            discord.SelectOption(
                label=str(uid),
                value=str(uid)
            )
            for uid in queue.data["queue"][:25]
        ]

        if not options:
            options = [
                discord.SelectOption(
                    label="（目前沒有玩家）",
                    value="0"
                )
            ]

        self.add_item(KickSelect(options))


# =========================
# 主 Queue View
# =========================

class QueueView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # =====================
    # 加入
    # =====================
    @discord.ui.button(label="🟢 加入", style=discord.ButtonStyle.green)
    async def join(self, interaction, button):

        queue.add_player(interaction.user.id)

        await interaction.response.send_message("✅ 已加入", ephemeral=True)

    # =====================
    # 離開
    # =====================
    @discord.ui.button(label="🔴 離開", style=discord.ButtonStyle.red)
    async def leave(self, interaction, button):

        queue.remove_player(interaction.user.id)

        await interaction.response.send_message("✅ 已離開", ephemeral=True)

    # =====================
    # 下一組
    # =====================
    @discord.ui.button(label="▶ 下一組", style=discord.ButtonStyle.blurple)
    async def next(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        queue.next_group()

        await interaction.response.send_message("🔔 已切換下一組", ephemeral=True)

    # =====================
    # 踢人（選單）
    # =====================
    @discord.ui.button(label="👢 踢人", style=discord.ButtonStyle.gray)
    async def kick(self, interaction, button):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ 無權限", ephemeral=True)

        await interaction.response.send_message(
            "選擇要踢出的玩家：",
            view=KickView(),
            ephemeral=True
        )


def get_persistent_views():
    return [QueueView()]
