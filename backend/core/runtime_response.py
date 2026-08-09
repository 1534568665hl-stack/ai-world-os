class RuntimeResponse:
    """Pure data wrapper for the unified world controller response."""

    def __init__(self, player_result, context, prompt):
        self.player_result = player_result
        self.context = context
        self.prompt = prompt

    def to_dict(self):
        return {
            "player_result": self.player_result,
            "context": self.context,
            "prompt": self.prompt,
        }
