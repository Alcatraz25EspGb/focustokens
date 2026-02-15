

class Ping:
    def __init__(self):
        self.sender_user_id = 0
        self.receiver_user_id = 0
        self.ping_type = ""
        self.message = ""
        self.cost = 0

    def setSenderUserId(self, sender_user_id) -> None:
        self.sender_user_id = sender_user_id

    def getSenderUserId(self) -> int:
        return self.sender_user_id
    
    def setReceiverUserId(self, receiver_user_id) -> None:
        self.receiver_user_id = receiver_user_id

    def getReceiverUserId(self) -> int:
        return self.receiver_user_id
    
    def setPingType(self, ping_type) -> None:
        self.ping_type = ping_type

    def getPingType(self) -> str:
        return self.ping_type
    
    def setMessage(self, message) -> None:
        self.message = message

    def getMessage(self) -> str:
        return self.message
    
    def setCost(self, cost) -> None:
        self.cost = cost

    def getCost(self) -> int:
        return self.cost
