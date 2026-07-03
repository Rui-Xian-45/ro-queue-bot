import discord


def build_embed(queue, guild):
    members = queue.data["members"]

    # =====================
    # 分組
    # =====================
    current = members[:3]
    next_group = members[3:6]
    waiting = members[6:]

    # =====================
    # 取得 Discord 暱稱
    # =====================
    def get_name(user_id):
        member = guild.get_member(user_id)
        return member.display_name if member else str(user_id)

    # =====================
    # 轉成文字
    # =====================
    current_text = (
        "\n".join(get_name(uid) for uid in current)
        if current else "（無）"
    )

    next_text = (
        "\n".join(get_name(uid) for uid in next_group)
        if next_group else "（無）"
    )

    waiting_text = (
        "\n".join(get_name(uid) for uid in waiting)
        if waiting else "（無）"
    )

    # =====================
    # Embed
    # =====================
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
