from __future__ import annotations

from datetime import date
from typing import Optional

from src.core.token_rules import refresh_balance_if_needed, spend

from src.data.user_repo import create_user, get_user_id
from src.data.settings_repo import ensure_default_settings, get_settings, update_settings
from src.data.balance_repo import init_balance_if_missing, get_balance, upsert_balance
from src.data.ping_repo import create_ping, get_pings_for_user, delete_ping

from src.models.settings import Settings


class FocusTokensApp:
    def __init__(self) -> None:
        """
        Docstring for __init__
        
        :param self: Description
        """
        # settings <- loaded at startup from database
        self.settings: Optional[Settings] = None

        # current_user_id <- set after selecting a user profile
        self.current_user_id: Optional[int] = None

    def start(self) -> None:
        """
        Docstring for start
        
        :param self: Description
        """
        # load system settings
        ensure_default_settings()
        row = get_settings()
        self.settings = Settings(
            daily_tokens=row["daily_tokens"],
            normal_ping_cost=row["normal_ping_cost"],
            urgent_ping_cost=row["urgent_ping_cost"],
        )

        # if Settings.validate() returns invalid -> display error and stop
        if not self.settings.validate():
            print("Invalid system settings.")
            return

        # display welcome message
        print("\nWelcome to FocusTokens (CLI)\n")

        # call select_user(username)
        if not self.select_user():
            print("User selection failed.")
            return

        # while the application is running: display menu options and read user choices
        running = True
        while running:
            print("\n--- Main Menu ---")
            print("1) Send ping")
            print("2) View balance")
            print("3) View history")
            print("4) Change settings")
            print("5) Exit")

            choice = input("Choose an option: ").strip()

            # if user choice is “Send Ping” -> handle_send_ping()
            if choice == "1":
                self.handle_send_ping()

            # else if user choice is “View balance” -> handle_view_balance()
            elif choice == "2":
                self.handle_view_balance()

            # else if user choice is “View history” -> handle_view_history()
            elif choice == "3":
                self.handle_view_history()

            # else if user choice is “Change settings” -> handle_change_settings()
            elif choice == "4":
                self.handle_change_settings()

            # else if user choice is “Exit” -> stop running
            elif choice == "5":
                running = False

            # otherwise -> display invalid option
            else:
                print("Invalid option.")

        # display “Goodbye!”
        print("\nGoodbye!\n")

    def select_user(self) -> bool:
        """
        Docstring for select_user
        
        :param self: Description
        :return: Description
        :rtype: bool
        """
        # read username
        username = input("Enter username to select: ").strip()

        # if username is empty -> display invalid username and return failure
        if username == "":
            print("Invalid username.")
            return False

        # find user_id by username
        user_id = get_user_id(username)

        # if the user is not found -> create a new user -> find user_id again
        if user_id is None:
            create_user(username)
            user_id = get_user_id(username)

        # if still not found -> return failure
        if user_id is None:
            print("Could not create/select user.")
            return False

        # assign user_id to current_user_id
        self.current_user_id = user_id

        # display “User selected” and return success
        print(f"User selected: {username} (id={self.current_user_id})")
        return True

    def handle_send_ping(self) -> None:
        """
        Docstring for handle_send_ping
        
        :param self: Description
        """
        # if sender is not selected -> display error and return
        if self.current_user_id is None:
            print("No user selected.")
            return

        # load the settings and assign the value to settings
        if self.settings is None:
            print("Settings not loaded.")
            return

        # if Settings.validate() returns invalid -> display error and return failure
        if not self.settings.validate():
            print("Invalid system settings.")
            return

        # read receiver username
        receiver_username = input("Receiver username: ").strip()

        # if receiver username is empty -> display error and return failure
        if receiver_username == "":
            print("Receiver username required.")
            return

        # find receiver id by receiver username
        receiver_id = get_user_id(receiver_username)

        # if receiver id is not found -> display “Receiver not found” and return failure
        if receiver_id is None:
            print("Receiver not found.")
            return

        # read ping type
        ping_type = input("Ping type (normal/urgent): ").strip().lower()

        # if ping type is not normal and not urgent -> display invalid ping type and return failure
        cost = self.settings.determine_cost(ping_type)
        if cost is None:
            print("Invalid ping type.")
            return

        # read optional message (empty -> None)
        message_raw = input("Optional message (press Enter for none): ").strip()
        message = message_raw if message_raw != "" else None

        # load token account for sender id
        today = date.today()
        today_str = today.isoformat()

        # if token account is not found -> create token account with daily tokens and set to today
        init_balance_if_missing(self.current_user_id, self.settings.daily_tokens, today_str)
        row = get_balance(self.current_user_id)
        if row is None:
            print("Could not load token balance.")
            return

        balance = int(row["balance"])
        last_refresh = date.fromisoformat(row["last_refresh"])

        # call refresh_if_needed(today, daily_tokens)
        balance, last_refresh = refresh_balance_if_needed(
            balance=balance,
            daily_tokens=self.settings.daily_tokens,
            last_refresh=last_refresh,
            today=today,
        )

        # if canSpend(cost) returns false -> display “Insufficient tokens” and return failure
        result = spend(balance=balance, cost=cost)
        if not result.success:
            if result.reason == "insufficient_tokens":
                print("Insufficient tokens.")
            else:
                print("Invalid cost.")
            return

        # save token account (updated balance and last refresh)
        upsert_balance(self.current_user_id, result.new_balance, last_refresh.isoformat())

        # create ping record and save ping
        create_ping(
            sender_user_id=self.current_user_id,
            receiver_user_id=receiver_id,
            ping_type=ping_type,
            message=message,
            cost=cost,
        )

        # display “Ping sent successfully”
        print("Ping sent successfully.")

    def handle_view_balance(self) -> None:
        """
        Docstring for handle_view_balance
        
        :param self: Description
        """
        # load the settings and assign to settings
        if self.current_user_id is None:
            print("No user selected.")
            return
        if self.settings is None:
            print("Settings not loaded.")
            return

        # load the token account for userId
        today = date.today()
        today_str = today.isoformat()

        # if token account is not found -> create token account with daily tokens and set to today
        init_balance_if_missing(self.current_user_id, self.settings.daily_tokens, today_str)
        row = get_balance(self.current_user_id)
        if row is None:
            print("Could not load token balance.")
            return

        balance = int(row["balance"])
        last_refresh = date.fromisoformat(row["last_refresh"])

        # call refresh_if_needed(today, dailyTokens)
        new_balance, new_last_refresh = refresh_balance_if_needed(
            balance=balance,
            daily_tokens=self.settings.daily_tokens,
            last_refresh=last_refresh,
            today=today,
        )

        # save token account
        if new_balance != balance or new_last_refresh != last_refresh:
            upsert_balance(self.current_user_id, new_balance, new_last_refresh.isoformat())

        # display the balance
        print("\n--- Balance ---")
        print(f"Balance: {new_balance}")
        print(f"Last refresh date: {new_last_refresh.isoformat()}")

    def handle_view_history(self) -> None:
        """
        Docstring for handle_view_history
        
        :param self: Description
        """
        # if limit is not provided -> set limit to 20
        # if limit is less than or equal to 0 -> display invalid limit and return empty list
        if self.current_user_id is None:
            print("No user selected.")
            return

        user_input = input("Enter ping display limit (press Enter for default 20): ").strip()
        if user_input == "":
            limit = 20
        else:
            try:
                limit = int(user_input)
            except ValueError:
                print("Invalid limit.")
                return
            if limit <= 0 or limit > 100:
                print("Invalid limit.")
                return

        # load recent pings for userId with LIMIT set to limit and assign it to pings
        pings = get_pings_for_user(self.current_user_id, limit)

        # display pings
        if not pings:
            print("You currently have no pings.")
            return

        print("\n--- Ping History ---")
        for r in pings:
            msg = r["message"] if r["message"] is not None else "(no message)"
            print(
                f"ID={r['id']} | type={r['ping_type']} | "
                f"from={r['sender_user_id']} to={r['receiver_user_id']} | "
                f"cost={r['cost']} | at={r['created_at']} | msg={msg}"
            )

        # user may close history or decide to delete a ping
        while True:
            action = input("\n[D]elete a ping or [B]ack: ").strip().lower()
            if action == "b":
                return
            if action == "d":
                self.handle_delete_ping(pings)
                return
            print("Invalid option.")

    def handle_delete_ping(self, displayed_pings) -> None:
        """
        Docstring for handle_delete_ping
        
        :param self: Description
        :param displayed_pings: Description
        """
        # display list already shown in history
        # ask for ping id to delete
        # if ping id is not in returned list -> display error and return
        # else call delete_ping
        # display success/fail message

        if self.current_user_id is None:
            print("No user selected.")
            return

        ping_id_str = input("Enter ping id to delete: ").strip()
        try:
            ping_id = int(ping_id_str)
        except ValueError:
            print("Invalid ping id.")
            return

        displayed_ids = {int(r["id"]) for r in displayed_pings}
        if ping_id not in displayed_ids:
            print("Ping id not in displayed list.")
            return

        # only delete pings that were sent by current user (matches repo delete rule)
        ping_row = None
        for r in displayed_pings:
            if int(r["id"]) == ping_id:
                ping_row = r
                break

        if ping_row is None:
            print("Ping not found.")
            return

        if int(ping_row["sender_user_id"]) != self.current_user_id:
            print("Cannot delete a ping that was not sent by current user.")
            return

        ok = delete_ping(self.current_user_id, ping_id)
        if ok:
            print("Ping deleted successfully.")
        else:
            print("Failed to delete ping.")

    def handle_change_settings(self) -> None:
        """
        Docstring for handle_change_settings
        
        :param self: Description
        """
        # display current settings values
        # read new values (blank -> keep current)
        # validate values using Settings.validate()
        # save settings to database
        # reload settings from database

        if self.settings is None:
            print("Settings not loaded.")
            return

        print("\n--- Current Settings ---")
        print(f"Daily tokens: {self.settings.daily_tokens}")
        print(f"Normal ping cost: {self.settings.normal_ping_cost}")
        print(f"Urgent ping cost: {self.settings.urgent_ping_cost}")

        new_daily = input("New daily tokens (blank to keep): ").strip()
        new_normal = input("New normal ping cost (blank to keep): ").strip()
        new_urgent = input("New urgent ping cost (blank to keep): ").strip()

        daily_tokens = self.settings.daily_tokens
        normal_cost = self.settings.normal_ping_cost
        urgent_cost = self.settings.urgent_ping_cost

        try:
            if new_daily != "":
                daily_tokens = int(new_daily)
            if new_normal != "":
                normal_cost = int(new_normal)
            if new_urgent != "":
                urgent_cost = int(new_urgent)
        except ValueError:
            print("Invalid numeric input.")
            return

        candidate = Settings(daily_tokens, normal_cost, urgent_cost)
        if not candidate.validate():
            print("Invalid settings.")
            return

        update_settings(daily_tokens, normal_cost, urgent_cost)

        row = get_settings()
        self.settings = Settings(
            daily_tokens=row["daily_tokens"],
            normal_ping_cost=row["normal_ping_cost"],
            urgent_ping_cost=row["urgent_ping_cost"],
        )

        print("Settings updated successfully.")
