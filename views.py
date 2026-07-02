import discord
from queue_manager import QueueManager

queue = QueueManager()


# =========================
# 玩家按鈕
# =========================

class PlayerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🟢 加入排隊", style=discord.ButtonStyle.green, custom_id="join_queue")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = queue.add_player(interaction.user.display_name)

        if result == "locked":
            await interaction.response.send_message("❌ 目前暫停排隊", ephemeral=True)
        elif result == "exists":
            await interaction.response.send_message("❌ 你已在隊列中", ephemeral=True)
        elif result == "full":
            await interaction.response.send_message("❌ 隊列已滿（30人）", ephemeral=True)
        else:
            await interaction.response.send_message("✅ 已加入排隊", ephemeral=True)

    @discord.ui.button(label="🔴 離開排隊", style=discord.ButtonStyle.red, custom_id="leave_queue")
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        ok = queue.remove_player(interaction.user.display_name)

        if ok:
            await interaction.response.send_message("✅ 已離開隊列", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 你不在隊列中", ephemeral=True)


# =========================
# 管理員面板
# =========================

class AdminView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # 下一組
    @discord.ui.button(label="▶ 下一組", style=discord.ButtonStyle.blurple, custom_id="next_group")
    async def next_group(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ 你沒有權限", ephemeral=True)
            return

        players = queue.next_group()

        if not players:
            await interaction.response.send_message("⚠ 沒有人在排隊", ephemeral=True)
            return

        mention = " ".join([f"@{p}" for p in players])

        await interaction.response.send_message(
            f"🔔 下一組進場：\n{mention}",
            allowed_mentions=discord.AllowedMentions(users=True)
        )

    # 鎖定
    @discord.ui.button(label="🔒 鎖定", style=discord.ButtonStyle.gray, custom_id="lock_queue")
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ 沒權限", ephemeral=True)
            return

        queue.lock()
        await interaction.response.send_message("🔒 已鎖定排隊", ephemeral=True)

    # 解鎖
    @discord.ui.button(label="🔓 開放", style=discord.ButtonStyle.gray, custom_id="unlock_queue")
    async def unlock(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ 沒權限", ephemeral=True)
            return

        queue.unlock()
        await interaction.response.send_message("🔓 已開放排隊", ephemeral=True)

    # 清空
    @discord.ui.button(label="🗑 清空", style=discord.ButtonStyle.red, custom_id="clear_queue")
    async def clear(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ 沒權限", ephemeral=True)
            return

        queue.clear()
        await interaction.response.send_message("🗑 已清空隊列", ephemeral=True)


# =========================
# 取得畫面用
# =========================

def get_player_view():
    return PlayerView()

def get_admin_view():
    return AdminView()
