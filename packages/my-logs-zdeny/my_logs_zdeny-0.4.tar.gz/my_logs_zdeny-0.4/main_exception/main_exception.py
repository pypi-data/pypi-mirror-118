import sys
import logging

logging.basicConfig(filename="my_logs.txt",level="DEBUG")
logging.debug("first debug message")
logging.info("first info debug")
logging.error("first error log")

print("ale tohle se stane na zacatku")

def tohle_nedelej():
    print("this is example")

class MyError(Exception):
    pass

def tohle_taky_nedelej():
    print (sys.platform)
    assert("win32" in sys.platform)

def my_error_test_func(tested_value):
    if tested_value > 5: 
        raise MyError("invalid level")
    else:
        print("vse ok",  tested_value)

if __name__ == "__main__":
    my_error_test_func(5)
