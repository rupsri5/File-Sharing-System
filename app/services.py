from app.exception import InputException


def validate_input(user_input, required_params, temporary_params=[]):
    for required_key in required_params:
        if required_key not in user_input.keys():
            raise InputException(f"Invalid input, {required_key} is required.")
    
    for key in user_input.keys():
        if key not in required_params and key not in temporary_params:
            raise InputException(f"Invalid input, {key} is not allowed.")
        if type(user_input[key])!=str:
            raise InputException(f"Invalid input, all values must be string.")
        