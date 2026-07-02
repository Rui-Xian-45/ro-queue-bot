import discord

def build_embed(queue, guild):

    members = queue.data["members"]
    i = queue.data["current_index"]

    current = members[i:i+3]
    next_group = members[i+3:i+6]

    def name(uid):
        member = guild.get_member(uid)
        return member.mention if member else f"<@{uid}>"

    return discord.Embed(
        title="⚔ RO 副本排隊系統",
        description=
        f"👥 人數：{len(members)}/25\n\n"
        f"🎮 副本中：{' '.join([name(u) for u in current]) if current else '空'}\n\n"
        f"➡ 下一組：{' '.join([name(u) for u in next_group]) if next_group else '空'}",
        color=discord.Color.green()
    )
