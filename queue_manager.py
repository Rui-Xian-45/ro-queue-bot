class QueueManager:
    def __init__(self):
        self.data = {
            "owner_id": None,
            "members": [],
            "locked": False,
            "current_index": 0,
            "message_id": None,
            "channel_id": None
        }

    # =====================
    # 建房
    # =====================
    def create_room(self, owner_id):
        self.data["owner_id"] = owner_id
        self.data["members"] = []
        self.data["current_index"] = 0

    # =====================
    # 加入
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
    # 離開
    # =====================
    def remove_player(self, user_id):
        if user_id in self.data["members"]:
            self.data["members"].remove(user_id)

    # =====================
    # 當前 3 人
    # =====================
    def get_current_group(self):
        i = self.data["current_index"]
        return self.data["members"][i:i+3]

    # =====================
    # 完成副本（3人一組前進）
    # =====================
    def finish_run(self):
        self.data["current_index"] += 3

        # 如果超過就重置
        if self.data["current_index"] >= len(self.data["members"]):
            self.data["current_index"] = 0

    # =====================
    # 踢人
    # =====================
    def kick_player(self, user_id):
        if user_id in self.data["members"]:
            self.data["members"].remove(user_id)
            return True
        return False

    # =====================
    # 鎖房
    # =====================
    def lock(self):
        self.data["locked"] = True

    def unlock(self):
        self.data["locked"] = False
