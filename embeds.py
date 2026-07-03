import discord

def build_embed(queue, guild):

    members = queue.data["members"]
    i = queue.data["current_index"]

    current = members[i:i+3]
    next_group = members[i+3:i+6]
    waiting = members[i+6:]

    def get_name(uid):
        member = guild.get_member(uid)
        return member.display_name if member else str(uid)

    current_text = "\n".join(get_name(uid) for uid in current) if current else "（無）"
    next_text = "\n".join(get_name(uid) for uid in next_group) if next_group else "（無）"
    waiting_text = "\n".join(get_name(uid) for uid in waiting) if waiting else "（無）"

    embed = discord.Embed(
        title="⚔ RO 副本排隊系統",
        color=discord.Color.green()
    )

    embed.add_field(
        name="👥 排隊人數",
        value=f"{len(members)}/25",
        inline=False
    )

    embed.add_field(
        name="🎮 副本中",
        value=current_text,
        inline=False
    )

    embed.add_field(
        name="⏭ 下一組",
        value=next_text,
        inline=False
    )

    embed.add_field(
        name="🕒 等候中",
        value=waiting_text,
        inline=False
    )

    return embed
