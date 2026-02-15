

class Settings:
    def __init__(self):
        self.daily_tokens = 30
        self.normal_ping_cost = 1
        self.urgent_ping_cost = 3

    def setDailyTokens(self, daily_tokens: int) -> None:
        self.daily_tokens = daily_tokens

    def getDailyTokens(self) -> int:
        return self.daily_tokens
    
    def setNormalPingCost(self, normal_cost: int) -> None:
        self.normal_ping_cost = normal_cost

    def getNormalPingCost(self) -> int:
        return self.normal_ping_cost
    
    def setUrgentPingCost(self, urgent_cost: int) -> None:
        self.urgent_ping_cost = urgent_cost

    def getUrgentPingCost(self) -> int:
        return self.urgent_ping_cost
    
    def determineCost(self, ping_type) -> int | None:
        if ping_type == "normal":
            return self.normal_ping_cost
        elif ping_type == "urgent":
            return self.urgent_ping_cost
        else:
            return None