import sys


def some_function():
    try:
        10 / 0  # Division by zero raises an exception
        print('' + 1)  # Type error
        pass
    except ZeroDivisionError as z:
        print("Oops, invalid > {}".format(z))
    except Exception as e:
        print("Unexpected error:", e)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print("Exception didn't occur, we're good.")
    finally:
        # This is executed after the code block is run
        # and all exceptions have been handled, even
        # if a new exception is raised while handling.
        print("We're done with that.")

some_function()
