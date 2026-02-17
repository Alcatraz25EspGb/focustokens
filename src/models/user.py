class User:
    def __init__(self, user_id: int, username: str):
        # store user id
        self.user_id = user_id

        # store username
        self.username = username

    def view_balance(self) -> None:
        # user requests to view token balance
        # controller handles token refresh and balance display
        pass

    def send_ping(self) -> None:
        # user requests to send a ping
        # controller handles receiver lookup, cost calculation, spending, and ping creation
        pass

    def view_history(self) -> None:
        # user requests to view ping history
        # controller loads and displays history and optional delete action
        pass
