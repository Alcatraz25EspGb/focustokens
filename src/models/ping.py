class Ping:
    def __init__(
        self,
        ping_id: int | None,
        sender_user_id: int,
        receiver_user_id: int,
        ping_type: str,
        cost: int,
        message: str | None = None,
        created_at: str | None = None,
    ):
        """
        Docstring for __init__
        
        :param self: Description
        :param ping_id: Description
        :type ping_id: int | None
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
        :param created_at: Description
        :type created_at: str | None
        """
        # store ping id (None if not assigned yet)
        self.ping_id = ping_id

        # store sender user id
        self.sender_user_id = sender_user_id

        # store receiver user id
        self.receiver_user_id = receiver_user_id

        # store ping type (normal/urgent)
        self.ping_type = ping_type

        # store optional message (None means no message)
        self.message = message

        # store cost
        self.cost = cost

        # store created timestamp (None if not assigned yet)
        self.created_at = created_at

    @classmethod
    def create(
        cls,
        sender_user_id: int,
        receiver_user_id: int,
        ping_type: str,
        message: str | None,
        cost: int,
    ) -> "Ping" | None:
        """
        Docstring for create
        
        :param cls: Description
        :param sender_user_id: Description
        :type sender_user_id: int
        :param receiver_user_id: Description
        :type receiver_user_id: int
        :param ping_type: Description
        :type ping_type: str
        :param message: Description
        :type message: str | None
        :param cost: Description
        :type cost: int
        :return: Description
        :rtype: Ping | None
        """
        # if sender_user_id is invalid or receiver_user_id is invalid -> return failure
        if sender_user_id <= 0 or receiver_user_id <= 0:
            return None

        # if ping type is not normal and ping type is not urgent -> return failure
        if ping_type not in ("normal", "urgent"):
            return None

        # if cost is less than 1 -> return failure
        if cost < 1:
            return None

        # create a new Ping object (ping_id and created_at assigned by persistence layer)
        return cls(
            ping_id=None,
            sender_user_id=sender_user_id,
            receiver_user_id=receiver_user_id,
            ping_type=ping_type,
            cost=cost,
            message=message,
            created_at=None,
        )

    def to_display_string(self) -> str:
        """
        Docstring for to_display_string
        
        :param self: Description
        :return: Description
        :rtype: str
        """
        # display "Ping Type: " + ping_type
        # display "From User ID: " + sender_user_id
        # display "To User ID: " + receiver_user_id
        # display "Message: " + message
        # display "Cost: " + cost
        # display "Sent At: " + created_at

        msg = self.message if self.message is not None and self.message != "" else "(no message)"
        created = self.created_at if self.created_at is not None else "(unknown time)"

        return (
            f"Ping Type: {self.ping_type}\n"
            f"From User ID: {self.sender_user_id}\n"
            f"To User ID: {self.receiver_user_id}\n"
            f"Message: {msg}\n"
            f"Cost: {self.cost}\n"
            f"Sent At: {created}"
        )
