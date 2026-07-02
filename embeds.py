import discord
from queue_manager import QueueManager
from datetime import datetime

queue = QueueManager()


def build_embed():

    data = queue.status()
    current = data["current"]
    q = data["queue"]

    embed = discord.Embed(
        title="🏰 RO 副本排隊系統",
        color=0x2ecc71
    )

    embed.add_field(
        name=f"👥 人數：{data['size']} / 30",
        value="━━━━━━━━━━━━",
        inline=False
    )

    embed.add_field(
        name="🟢 進行中（3人）",
        value="\n".join(current) if current else "（無）",
        inline=False
    )

    embed.add_field(
        name="🟡 下一組",
        value="\n".join(q[:3]) if q else "（無）",
        inline=False
    )

    embed.add_field(
        name="⚪ 排隊中",
        value="\n".join(q[3:]) if len(q) > 3 else "（無）",
        inline=False
    )

    embed.set_footer(text=f"更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return embed
