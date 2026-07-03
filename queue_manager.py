class QueueManager:

    def __init__(self):
        self.data = {
            "members": [],
            "locked": False,
            "message_id": None,
            "channel_id": None,
        }

    # =====================
    # 加入排隊
    # =====================
    def add_player(self, user_id):

        if self.data["locked"]:
            return "locked"

        if user_id in self.data["members"]:
            return "exists"

        if len(self.data["members"]) >= 25:
            return "full"

        self.data["members"].append(user_id)
        return "ok"

    # =====================
    # 離開排隊
    # =====================
    def remove_player(self, user_id):

        if user_id in self.data["members"]:
            self.data["members"].remove(user_id)

    # =====================
    # 踢除玩家
    # =====================
    def kick_player(self, user_id):

        if user_id in self.data["members"]:
            self.data["members"].remove(user_id)
            return True

        return False

    # =====================
    # 完成副本（移除前三位）
    # =====================
    def finish_run(self):

        # 沒有人
        if not self.data["members"]:
            return

        # 移除副本中的前三人
        del self.data["members"][:3]

    # =====================
    # 鎖房
    # =====================
    def lock(self):
        self.data["locked"] = True

    # =====================
    # 解鎖
    # =====================
    def unlock(self):
        self.data["locked"] = False
