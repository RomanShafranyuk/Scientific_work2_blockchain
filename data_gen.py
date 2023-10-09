import random
import string
import secrets

def get_random_string(length: int)-> list:
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(length)) 
def generate_block_data(count_blocks: int, len_names: int, start_interval: int, end_interval:int, keys: list) -> list:
    result = []
    for _ in range(count_blocks):
        result.append({keys[0]: get_random_string(len_names), keys[1]: random.randint(start_interval, end_interval + 1), keys[2]: get_random_string(len_names)})
    return result


