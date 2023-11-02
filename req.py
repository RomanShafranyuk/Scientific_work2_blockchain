import requests
from multiprocessing import Pool
import data_gen
import block
import database

def request_to_blocks(data):
    requests.post("http://25.22.250.163:5000", data)

NAMES_LENGTH = 5
MINIMAL_SUM = 1000
MAX_SUM = 10000000
KEYS = ["lender", "amount", "borrower"]





if __name__ == "__main__":
    for i in range(1000, 5001, 500):
        data_blocks = data_gen.generate_block_data(i, NAMES_LENGTH, MINIMAL_SUM, MAX_SUM, KEYS)
        with Pool(4) as p:
            p.map(request_to_blocks, data_blocks)
        block.get_average_time(i)
        database.clear_tables(database.create_session())
         
  
