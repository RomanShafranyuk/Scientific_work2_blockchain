import requests
from multiprocessing import Pool
from threading import Lock
import data_gen
import database
import block

BLOCK_COUNT = 10000
NAMES_LENGTH = 5
MINIMAL_SUM = 1000
MAX_SUM = 10000000
KEYS = ["lender", "amount", "borrower"]
time = []
time_lock = Lock()

def request_to_blocks(data):
    time_to_add = requests.post("http://127.0.0.1:5000", data).data
    time_lock.acquire()
    time.append(time_to_add["time"])
    time_lock.release()


if __name__ == "__main__":
    data_blocks = data_gen.generate_block_data(BLOCK_COUNT, NAMES_LENGTH, MINIMAL_SUM, MAX_SUM, KEYS)
    with Pool(4) as p:
        p.map(request_to_blocks, data_blocks)
    for value in time:
        database.add_time(value)
    block.get_average_time(BLOCK_COUNT) 
  
