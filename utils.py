# utility functions to be reused

def verify_fields(*args):
    # Check each argument to see if it's None or an empty string
    for input_value in args:
        if input_value is None or input_value == "":
            return False
    return True