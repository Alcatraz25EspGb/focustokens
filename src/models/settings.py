class Settings:
    def __init__(self, daily_tokens: int, normal_ping_cost: int, urgent_ping_cost: int):
        """
        Docstring for __init__
        
        :param self: Description
        :param daily_tokens: Description
        :type daily_tokens: int
        :param normal_ping_cost: Description
        :type normal_ping_cost: int
        :param urgent_ping_cost: Description
        :type urgent_ping_cost: int
        """
        # store daily tokens, normal ping cost, urgent ping cost
        self.daily_tokens = daily_tokens
        self.normal_ping_cost = normal_ping_cost
        self.urgent_ping_cost = urgent_ping_cost

    def determine_cost(self, ping_type: str) -> int | None:
        """
        Docstring for determine_cost
        
        :param self: Description
        :param ping_type: Description
        :type ping_type: str
        :return: Description
        :rtype: int | None
        """
        # if ping type is normal -> return normal ping cost
        if ping_type == "normal":
            return self.normal_ping_cost

        # else if ping type is urgent -> return urgent ping cost
        if ping_type == "urgent":
            return self.urgent_ping_cost

        # otherwise -> return invalid
        return None

    def validate(self) -> bool:
        """
        Docstring for validate
        
        :param self: Description
        :return: Description
        :rtype: bool
        """
        # if daily tokens is less than 1 -> invalid
        if self.daily_tokens < 1:
            return False

        # if normal ping cost is less than 1 -> invalid
        if self.normal_ping_cost < 1:
            return False

        # if urgent ping cost is less than normal ping cost -> invalid
        if self.urgent_ping_cost < self.normal_ping_cost:
            return False

        # otherwise -> valid
        return True
