import time
import random

def sleep(_min=1, _max=9):
    rand_float = random.uniform(_min, _max)
    print(f"This machine will sleep {round(rand_float, 2)} second")
    time.sleep(rand_float)