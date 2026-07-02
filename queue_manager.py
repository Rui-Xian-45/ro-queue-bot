import json
from typing import List


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

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except:
            self.save()

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_queue(self):
        return self.data["queue"]

    def get_current(self):
        return self.data["current"]

    def add_player(self, name: str):
        if self.data["locked"]:
            return "locked"

        if name in self.data["queue"] or name in self.data["current"]:
            return "exists"

        if len(self.data["queue"]) + len(self.data["current"]) >= self.max_size:
            return "full"

        self.data["queue"].append(name)
        self.save()
        return "ok"

    def remove_player(self, name: str):
        if name in self.data["queue"]:
            self.data["queue"].remove(name)
            self.save()
            return True

        if name in self.data["current"]:
            self.data["current"].remove(name)
            self.save()
            return True

        return False

    def next_group(self):
        self.data["current"] = self.data["queue"][:self.group_size]
        self.data["queue"] = self.data["queue"][self.group_size:]
        self.save()
        return self.data["current"]

    def clear(self):
        self.data["queue"] = []
        self.data["current"] = []
        self.save()

    def lock(self):
        self.data["locked"] = True
        self.save()

    def unlock(self):
        self.data["locked"] = False
        self.save()

    def status(self):
        return {
            "queue": self.data["queue"],
            "current": self.data["current"],
            "size": len(self.data["queue"]) + len(self.data["current"]),
            "locked": self.data["locked"]
        }
