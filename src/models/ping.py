

class Ping:
    # Take input from handleSendPing
    def __init__(self, sender_user_id: int, receiver_user_id: int, ping_type: str, cost: int, message: str | None = None):
        """
        Docstring for __init__
        
        :param self: Description
        :param sender_user_id: Description
        :type sender_user_id: int
        :param receiver_user_id: Description
        :type receiver_user_id: int
        :param ping_type: Description
        :type ping_type: str
        :param cost: Description
        :type cost: int
        :param message: Description
        :type message: str | None
        """
        self.sender_user_id = sender_user_id
        self.receiver_user_id = receiver_user_id
        self.ping_type = ping_type
        self.cost = cost
        self.message = message
        

    
