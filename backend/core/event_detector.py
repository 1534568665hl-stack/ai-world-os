class EventDetector:
    """Detect small, deterministic player events from plain text."""

    EVENT_RULES = (
        ("help", ("帮助", "帮忙", "修理", "解决", "协助", "救"), 5),
        ("chat", ("你好", "聊天", "聊聊", "说话", "交流"), 1),
        ("gift", ("送你", "礼物", "赠送", "给你"), 3),
        ("conflict", ("讨厌", "生气", "争吵", "攻击"), 5),
    )

    NPC_ALIASES = {
        "沫沫": "N_Momo",
        "momo": "N_Momo",
        "N_Momo": "N_Momo",
    }

    def _detect_target(self, user_input):
        normalized_input = user_input.casefold()
        for alias, npc_id in self.NPC_ALIASES.items():
            if alias.casefold() in normalized_input:
                return npc_id
        return ""

    def detect(self, user_input):
        """Return one normalized event, or an empty event when unmatched."""
        text = user_input or ""
        target = self._detect_target(text)

        for event_type, keywords, value in self.EVENT_RULES:
            if any(keyword in text for keyword in keywords):
                return {
                    "event_type": event_type,
                    "target": target,
                    "value": value,
                    "source": "player",
                }

        return {
            "event_type": "",
            "target": target,
            "value": 0,
            "source": "player",
        }
