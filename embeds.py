import discord

def build_embed(queue, guild: discord.Guild = None):

    members = queue.data["members"]
    i = queue.data["current_index"]

    current_ids = members[i:i+3]
    next_ids = members[i+3:i+6]

    # ⭐ 轉名字
    def get_name(uid):
        if guild:
            member = guild.get_member(uid)
            if member:
                return member.display_name
        return str(uid)

    current = [get_name(uid) for uid in current_ids]
    next_group = [get_name(uid) for uid in next_ids]

    return discord.Embed(
        title="⚔ RO 副本排隊系統",
        description=(
            f"👥 人數：{len(members)}/25\n\n"
            f"🎮 副本中：{current}\n\n"
            f"➡ 下一組：{next_group}"
        ),
        color=discord.Color.green()
    )
