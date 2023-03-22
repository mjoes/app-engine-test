import time
import logging 


def function_test():
    i=0
    k=0
    while i < 10:
        k=k+1
        time.sleep(1)
        logging.info(f"logging {k}")
        print(f"test print no: {k}")

if __name__ == '__main__':
    function_test()