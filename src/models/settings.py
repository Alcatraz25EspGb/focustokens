

class Settings:
    # This is a constructor to store the database settings values
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
        self.daily_tokens: int = daily_tokens
        self.normal_ping_cost: int = normal_ping_cost
        self.urgent_ping_cost: int = urgent_ping_cost
    
    # This function determines the cost of the ping base on the ping type
    def determineCost(self, ping_type: str) -> int | None: 
        """
        Docstring for determineCost
        
        :param self: Description
        :param ping_type: Description
        :type ping_type: str
        :return: Description
        :rtype: int | None
        """
        if ping_type == "normal":
            return self.normal_ping_cost # If the ping type is normal, then the normal ping cost is assigned 
        elif ping_type == "urgent":
            return self.urgent_ping_cost # If the ping type is urgent, then the urgent ping cost is assigned
        else:
            return None # If ping type is unknown, no value is assigned or returned 

    # This function validates the settings' values    
    def validate(self) -> bool: 
        """
        Docstring for validate
        
        :param self: Description
        :return: Description
        :rtype: bool
        """
        is_valid = True
        
        if self.daily_tokens < 0: # Check if daily tokens is nonnegative
            is_valid= False
            return is_valid
        if self.normal_ping_cost < 1: # Check if normal ping cost is greater than 1
            is_valid = False
            return is_valid
        if self.urgent_ping_cost < 1: # Check if urgent ping cost is grater than 1
            is_valid = False
            return is_valid
        if self.urgent_ping_cost < self.normal_ping_cost: # Check if urgent ping cost is greater than normal ping cost
            is_valid = False
            return is_valid
        
        return is_valid # Return True if none of the above conditions are satisfied 
        