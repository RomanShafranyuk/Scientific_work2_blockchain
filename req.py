import requests
from multiprocessing import Pool
import data_gen
import database

BLOCK_COUNT = 1000
NAMES_LENGTH = 5
MINIMAL_SUM = 100000
MAX_SUM = 10000000
KEYS = ["lender", "amount", "borrower"]
def request_to_blocks(data):
    requests.post("http://127.0.0.1:5000", data)



if __name__ == "__main__":
    data_blocks = data_gen.generate_block_data(BLOCK_COUNT, NAMES_LENGTH, MINIMAL_SUM, MAX_SUM, KEYS)
    with Pool(4) as p:
        p.map(request_to_blocks, data_blocks)

    time_avg = database.get_average_time()

    with open('time.txt', "a") as f:
        f.write(str(BLOCK_COUNT) + ":" + str(time_avg)+'\n')

