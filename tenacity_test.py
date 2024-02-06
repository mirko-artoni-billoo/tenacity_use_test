import random
import logging
import time
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential_jitter,
)


def return_last_value(retry_state):
    """
    return the result of the last call attempt
    """
    return retry_state.outcome.result()


def log_attempt_number(retry_state: RetryCallState):
    """
    return the result of the last call attempt
    """
    if retry_state.attempt_number == 1:
        logging.error(
            f" Calling — time passed : {round(time.monotonic() - retry_state.start_time, 2)} seconds, attempts n°{retry_state.attempt_number}..."
        )
    else:
        logging.error(
            f" Retry — time passed : {round(time.monotonic() - retry_state.start_time, 2)} seconds, attempts n°{retry_state.attempt_number}..."
        )


@retry(
    before=log_attempt_number,
    stop=(stop_after_delay(180) | stop_after_attempt(5)),
    retry=retry_if_exception_type(TypeError),
    retry_error_callback=return_last_value,
    wait=wait_exponential_jitter(initial=3),
)
def do_something_unreliable():
    try:
        value = random.randint(0, 99)
        if value >= 80:
            print(f"Current value {value}, IOException exit!")
            raise IOError("Value above 80")
        elif value >= 10:
            print(f"Current value {value}.")
            raise TypeError("Value between 10 and 80")
        else:
            print(f"Current value {value}, OK!!")
            return {"code": 200, "response": "Good soup!"}

    except IOError as e:
        return {
            "code": 100,
            "response": f"Bad soup — {e}",
        }


try:
    print(do_something_unreliable())
except TypeError as e:
    print(
        {
            "code": 500,
            "response": f"Unable to retrieve response — {e}",
        }
    )
