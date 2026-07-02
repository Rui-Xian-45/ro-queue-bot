import json
from typing import Dict, List


class QueueManager:
    def __init__(self, file_path="data.json", max_size=30, group_size=3):
        self.file_path = file_path
        self.max_size = max_size
        self.group_size = group_size

        self.data = {
            "queue": [],
            "current": [],
            "locked": False,
            "message_id": None,
            "channel_id": None
        }

        self.load()

    # -----------------------
    # 基本資料處理
    # -----------------------
    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except:
            self.save()

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # -----------------------
    # 狀態查詢
    # -----------------------
    def get_queue(self) -> List[str]:
        return self.data["queue"]

    def get_current(self) -> List[str]:
        return self.data["current"]

    def is_locked(self) -> bool:
        return self.data["locked"]

    # -----------------------
    # 加入隊列
    # -----------------------
    def add_player(self, user_name: str) -> str:
        if self.data["locked"]:
            return "locked"

        if user_name in self.data["queue"] or user_name in self.data["current"]:
            return "exists"

        if len(self.data["queue"]) + len(self.data["current"]) >= self.max_size:
            return "full"

        self.data["queue"].append(user_name)
        self.save()
        return "ok"

    # -----------------------
    # 離開隊列
    # -----------------------
    def remove_player(self, user_name: str) -> bool:
        if user_name in self.data["queue"]:
            self.data["queue"].remove(user_name)
            self.save()
            return True

        if user_name in self.data["current"]:
            self.data["current"].remove(user_name)
            self.save()
            return True

        return False

    # -----------------------
    # 下一組（核心）
    # -----------------------
    def next_group(self) -> List[str]:
        self.data["current"] = []

        next_players = self.data["queue"][:self.group_size]
        self.data["current"] = next_players

        self.data["queue"] = self.data["queue"][self.group_size:]

        self.save()
        return next_players

    # -----------------------
    # 剔除玩家（管理員）
    # -----------------------
    def kick_player(self, user_name: str):
        if user_name in self.data["queue"]:
            self.data["queue"].remove(user_name)

        if user_name in self.data["current"]:
            self.data["current"].remove(user_name)

        self.save()

    # -----------------------
    # 清空隊列
    # -----------------------
    def clear(self):
        self.data["queue"] = []
        self.data["current"] = []
        self.save()

    # -----------------------
    # 鎖定 / 解鎖
    # -----------------------
    def lock(self):
        self.data["locked"] = True
        self.save()

    def unlock(self):
        self.data["locked"] = False
        self.save()

    # -----------------------
    # 統計
    # -----------------------
    def size(self):
        return len(self.data["queue"]) + len(self.data["current"])

    def status(self):
        return {
            "current": self.data["current"],
            "queue": self.data["queue"],
            "size": self.size(),
            "locked": self.data["locked"]
        }
