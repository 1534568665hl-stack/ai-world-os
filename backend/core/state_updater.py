class StateUpdater:

    def __init__(self):
        pass


    def detect(self, user_input):

        result = {}


        location_keywords = {

            "暖阳角落咖啡店":
                "L_Warm_Corner",

            "暖阳角落":
                "L_Warm_Corner",

            "咖啡店":
                "L_Warm_Corner"

        }


        for keyword, location_id in location_keywords.items():

            if keyword in user_input:

                result["location"] = location_id

                break



        return result
