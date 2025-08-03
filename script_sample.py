def print_hello():
    """Example reusable function that prints a greeting."""
    print("Hello world!")

def main(*args):
    """
    Main script function (required entry point).
    Processes command line arguments and executes appropriate functions.
    """
    if args[0] == "test":
        print_hello()
    else:
        print("No valid command provided.")
