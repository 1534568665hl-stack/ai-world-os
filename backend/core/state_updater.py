class StateUpdater:
    """
    根据玩家输入更新世界运行状态

    负责：
    - 检测地点
    - 检测NPC
    - 返回需要写入StateManager的数据
    """


    def __init__(self):
        pass



    def detect(self, user_input):

        result = {}


        # ==========================
        # Location Detection
        # ==========================

        location_keywords = {

            "暖阳角落咖啡店":
                "L_Warm_Corner",

            "暖阳角落":
                "L_Warm_Corner",

            "咖啡店":
                "L_Warm_Corner",

            "猫薄荷公寓":
                "catnip_apt_302",

            "302室":
                "catnip_apt_302"

        }


        for keyword, location_id in location_keywords.items():

            if keyword in user_input:

                result["location"] = location_id
                break



        # ==========================
        # NPC Detection
        # ==========================

        npc_keywords = {

            "沫沫":
                "momo",

            "Momo":
                "momo"

        }


        active_npc = []


        for keyword, npc_id in npc_keywords.items():

            if keyword in user_input:

                active_npc.append(npc_id)



        if active_npc:

            result["active_npc"] = active_npc



        return result
