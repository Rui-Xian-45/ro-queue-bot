import discord


def build_embed(queue):

    members = queue.data["members"]
    i = queue.data["current_index"]

    current = members[i:i+3]
    next_group = members[i+3:i+6]

    return discord.Embed(
        title="⚔ RO 副本排隊系統",
        description=(
            f"👥 人數：{len(members)}/25\n\n"
            f"🎮 副本中：{current}\n\n"
            f"➡ 下一組：{next_group}"
        ),
        color=discord.Color.green()
    )
