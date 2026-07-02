class QueueManager:
    def __init__(self):
        self.data = {
            "members": [],
            "locked": False,
            "current_index": 0,
            "message_id": None,
            "channel_id": None,
        }

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
    # 踢人
    # =====================
    def kick_player(self, user_id):
        self.remove_player(user_id)

    # =====================
    # 3人副本
    # =====================
    def get_current_group(self):
        i = self.data["current_index"]
        return self.data["members"][i:i+3]

    

    def finish_run(self):

    members = self.data["members"]
    i = self.data["current_index"]

    # 推進 index
    self.data["current_index"] += 3

    # 超過就處理
    if self.data["current_index"] >= len(members):
        self.data["current_index"] = len(members)  # 停在尾端

    
    # =====================
    # lock
    # =====================
    def lock(self):
        self.data["locked"] = True

    def unlock(self):
        self.data["locked"] = False
