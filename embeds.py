import discord

def build_embed(queue, guild: discord.Guild = None):

    members = queue.data["members"]
    i = queue.data["current_index"]

    current_ids = members[i:i+3]
    next_ids = members[i+3:i+6]

    # =====================
    # 轉 mention（重點）
    # =====================
    def to_mention(uid):
        member = guild.get_member(uid) if guild else None
        if member:
            return member.mention   # ⭐ @tag
        return f"<@{uid}>"          # fallback

    current = [to_mention(uid) for uid in current_ids]
    next_group = [to_mention(uid) for uid in next_ids]

    return discord.Embed(
        title="⚔ RO 副本排隊系統",
        description=(
            f"👥 人數：{len(members)}/25\n\n"
            f"🎮 副本中：{' '.join(current) if current else '空'}\n\n"
            f"➡ 下一組：{' '.join(next_group) if next_group else '空'}"
        ),
        color=discord.Color.green()
    )
