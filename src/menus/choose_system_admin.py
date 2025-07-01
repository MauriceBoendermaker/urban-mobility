from src.managers.system_admin_manager import list_system_admins

def choose_system_admin():
    Admins = list_system_admins()
    while True:
        choice = input("\nEnter the ID of the system admin you want to choose: ")
        if choice is None:
            print("Cancelled.")
            return None

        if choice.isdigit():
            choice = int(choice)
            for admin in Admins:
                if admin[0] == choice:
                    return admin[0]
            print("Invalid ID. Please try again.")
        else:
            print("Invalid input. Please enter a number.")
