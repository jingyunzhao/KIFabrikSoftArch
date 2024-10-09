# /home/fandibi/Desktop/Jingyun/KIFabrikSoftArch/supermarket_cell/comm_interface.py

# Predefined message catalog
message_catalog = {
    "WELCOME": "Welcome to the Supermarket!",
    "GOODBYE": "Thank you for visiting. Have a great day!",
    "ERROR": "An error has occurred. Please try again.",
    "OUT_OF_STOCK": "The item you requested is currently out of stock.",
    "PROMOTION": "Don't miss our special promotion on selected items!",
    "HELP": "For assistance, please contact our support team."
}

# Example usage
def get_message(key):
    return message_catalog.get(key, "Message not found.")

# Test the message catalog
if __name__ == "__main__":
    print(get_message("WELCOME"))
    print(get_message("GOODBYE"))
    print(get_message("UNKNOWN_KEY"))