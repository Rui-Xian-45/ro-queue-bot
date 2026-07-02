class QueueManager:
    def __init__(self):
        self.data = {
            "members": [],
            "room_admins": [],
            "locked": False,
            "current_index": 0,
            "message_id": None,
            "channel_id": None,
            "room_created": False
        }

    # =====================
    # 房間
    # =====================
    def create_room(self, owner_id=None):
        self.data["members"] = []
        self.data["room_admins"] = [owner_id] if owner_id else []
        self.data["current_index"] = 0
        self.data["locked"] = False

    # =====================
    # admin
    # =====================
    def add_room_admin(self, user_id):
        if user_id not in self.data["room_admins"]:
            self.data["room_admins"].append(user_id)

    def is_admin(self, user_id):
        return user_id in self.data["room_admins"]

    # =====================
    # queue
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

    def remove_player(self, user_id):
        if user_id in self.data["members"]:
            self.data["members"].remove(user_id)

    def kick_player(self, user_id):
        return self.remove_player(user_id)

    # =====================
    # 副本（3人）
    # =====================
    def get_current_group(self):
        i = self.data["current_index"]
        return self.data["members"][i:i+3]

    def finish_run(self):
        self.data["current_index"] += 3

        if self.data["current_index"] >= len(self.data["members"]):
            self.data["current_index"] = 0

    # =====================
    # lock
    # =====================
    def lock(self):
        self.data["locked"] = True

    def unlock(self):
        self.data["locked"] = False
