import requests
from multiprocessing import Pool
import time
import data_gen

BLOCK_COUNT = 100
NAMES_LENGTH = 5
MINIMAL_SUM = 100000
MAX_SUM = 10000000
KEYS = ["lender", "amount", "borrower"]
def request_to_blocks(data):
    requests.post("http://25.22.250.163:5000", data)



if __name__ == "__main__":
    data_blocks = data_gen.generate_block_data(BLOCK_COUNT, NAMES_LENGTH, MINIMAL_SUM, MAX_SUM, KEYS)
    start = time.time()
    with Pool(4) as p:
        p.map(request_to_blocks, data_blocks)
    end = time.time()

    print((end - start)/BLOCK_COUNT)
