def display_message():
    """Display a message indicating that the function is broken."""
    print("This is a broken function")


def evaluate_number(input_number):
    """Evaluate the input number and print a corresponding message.

    Args:
        input_number (int or float): The number to evaluate.
    """
    # Determine the message based on the value of input_number
    result_message = "Input number is greater than 10" if input_number > 10 else "Input number is less than or equal to 10"
    print(result_message)


display_message()
evaluate_number(5)