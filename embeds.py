import discord
from queue_manager import QueueManager
from datetime import datetime

queue = QueueManager()


# =========================
# 建立 RO 排隊畫面
# =========================

def build_embed():

    data = queue.status()

    current = data["current"]
    q = data["queue"]
    size = data["size"]

    embed = discord.Embed(
        title="🏰 RO 副本排隊",
        color=0x00ff99
    )

    embed.add_field(
        name=f"👥 目前排隊：{size} / 30",
        value="━━━━━━━━━━━━━━━━",
        inline=False
    )

    # -------------------------
    # 🟢 進行中
    # -------------------------
    current_text = "\n".join(
        [f"① {current[i]}" if i == 0 else
         f"② {current[i]}" if i == 1 else
         f"③ {current[i]}" if i == 2 else current[i]
         for i in range(len(current))]
    ) if current else "（無）"

    embed.add_field(
        name="🟢 副本進行中",
        value=current_text,
        inline=False
    )

    # -------------------------
    # 🟡 下一組
    # -------------------------
    next_group = q[:3]
    next_text = "\n".join(next_group) if next_group else "（無）"

    embed.add_field(
        name="🟡 下一組（準備）",
        value=next_text,
        inline=False
    )

    # -------------------------
    # ⚪ 排隊中
    # -------------------------
    waiting = q[3:]
    waiting_text = "\n".join(waiting) if waiting else "（無）"

    embed.add_field(
        name="⚪ 排隊中",
        value=waiting_text,
        inline=False
    )

    # -------------------------
    # 更新時間
    # -------------------------
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    embed.set_footer(text=f"🕒 更新時間：{now}")

    return embed
