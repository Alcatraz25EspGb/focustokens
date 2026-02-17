from datetime import date

from src.core.token_rules import SpendResult, can_spend, spend, refresh_balance_if_needed


class TokenAccount:
    def __init__(self, user_id: int, balance: int, last_refresh_date: date):
        """
        Docstring for __init__
        
        :param self: Description
        :param user_id: Description
        :type user_id: int
        :param balance: Description
        :type balance: int
        :param last_refresh_date: Description
        :type last_refresh_date: date
        """
        # store user id
        self.user_id = user_id

        # store balance
        self.balance = balance

        # store last refresh date
        self.last_refresh_date = last_refresh_date

    def refresh_if_needed(self, today: date, daily_tokens: int) -> None:
        """
        Docstring for refresh_if_needed
        
        :param self: Description
        :param today: Description
        :type today: date
        :param daily_tokens: Description
        :type daily_tokens: int
        """
        # if today is after last_refresh_date:
        #     assign daily tokens to balance
        #     assign today to last_refresh_date
        new_balance, new_last_refresh = refresh_balance_if_needed(
            balance=self.balance,
            daily_tokens=daily_tokens,
            last_refresh=self.last_refresh_date,
            today=today,
        )

        self.balance = new_balance
        self.last_refresh_date = new_last_refresh

    def can_spend(self, cost: int) -> bool:
        """
        Docstring for can_spend
        
        :param self: Description
        :param cost: Description
        :type cost: int
        :return: Description
        :rtype: bool
        """
        # if cost is less than 1 -> return false
        # return (balance is greater than or equal to cost)
        return can_spend(balance=self.balance, cost=cost)

    def spend(self, cost: int) -> SpendResult:
        """
        Docstring for spend
        
        :param self: Description
        :param cost: Description
        :type cost: int
        :return: Description
        :rtype: SpendResult
        """
        # if cost is less than 1 -> return failure("invalid_cost")
        # if balance is less than cost -> return failure("insufficient_tokens")
        # subtract cost from balance and return success(new balance)
        result = spend(balance=self.balance, cost=cost)

        if result.success:
            self.balance = result.new_balance

        return result
