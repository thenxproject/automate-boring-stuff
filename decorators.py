import time


def run_time(func):
    """Decorator that will calculate the run time of a method and print it to the console."""

    # Wrapper around the function used to calculate the run time.
    def wrapper(*args):
        # Gets the start time
        start = time.time()

        # Runs the function that the decorator was placed on.
        func_output = func(*args)

        # Gets the end time and subtracts the start time to get the run time.
        end = time.time()
        total = end - start

        # Rounds to hundredths of a second and prints the rn time to the console.
        total = round(total, 2)
        print(f"""The method {func.__name__} took {total} seconds to run.""")

        # Returns the output of the function.
        return func_output

    # Returns the output of the function from the wrapper.
    return wrapper
