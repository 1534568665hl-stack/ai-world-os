import re


class MemoryExtractor:

    def __init__(self):

        self.rules = [

            {
                "type": "preference",
                "patterns": [
                    r"我喜欢(.+)",
                    r"我喜欢喝(.+)",
                    r"我喜欢吃(.+)"
                ],
                "importance": 3
            },


            {
                "type": "dislike",
                "patterns": [
                    r"我不喜欢(.+)",
                    r"我讨厌(.+)"
                ],
                "importance": 3
            },


            {
                "type": "identity",
                "patterns": [
                    r"我是(.+)",
                    r"我叫(.+)"
                ],
                "importance": 4
            },


            {
                "type": "relationship",
                "patterns": [
                    r"(.+)是我的朋友",
                    r"(.+)和我是朋友"
                ],
                "importance": 4
            },


            {
                "type": "event",
                "patterns": [
                    r"第一次(.+)",
                    r"今天(.+)",
                    r"刚刚(.+)"
                ],
                "importance": 2
            }

        ]


    def extract(
        self,
        text
    ):

        memories = []


        for rule in self.rules:

            for pattern in rule["patterns"]:

                result = re.search(
                    pattern,
                    text
                )


                if result:

                    memories.append({

                        "type":
                            rule["type"],

                        "content":
                            text,

                        "importance":
                            rule["importance"]

                    })


        return memories
