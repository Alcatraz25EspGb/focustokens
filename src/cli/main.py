from src.data.ping_repo import get_pings_for_user, delete_ping

def delete_ping_flow(user_id: int) -> None:
    """
    Docstring for delete_ping_flow
    
    :param user_id: Description
    :type user_id: int
    """
    user_pings = []
    user_input = input("Enter ping display limit (press Entrer for default 20)").strip() # Read a string from user
    if user_input == "": # If the string is empty, then call the get_pings_for_user with user_id
        user_pings = get_pings_for_user(user_id) # Store the returned list of user pings
        if not user_pings:
            print("You currently have no pings") # Check if the user has pings
            return
    else:
        try:
            ping_limit = int(user_input) # Convert the string to integer
        except ValueError:
            print("Invalid input") # If the conversion fails, then print the failure message and return
            return 
        if ping_limit <= 0 or ping_limit > 100: # If negative, zero or greater than 100, it is invalid
            print("The number of pings to display cannot exceed 100 or be less than or equal to 0")
            return
        else: # Else call get_pings_for_user if the value is valid
            user_pings = get_pings_for_user(user_id, ping_limit)
            if not user_pings:
                print("You currently have no pings") # Check if the user has pings
                return
            

       
            
        
    
    # Display the list of pings
    # If the returned list is empty, display "No pings available" and return
    # Ask for ping id to delete
    # User choses the id from the returned list
    # If ping id is not in the returned list, display an error message and return
    # Else call delete_ping
        # Display success/fail message