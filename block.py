import json
import os
import hashlib
import database

blockchain_dir = os.curdir + '/blocks/'


def get_hash(filename: str) -> str:
    file = open(blockchain_dir + filename, 'rb').read()
    print(file)
    return hashlib.sha256(file).hexdigest()


def get_hash_db():
    data_prev_block = database.get_block_data()
    data_to_json = json.dumps(
        {'name': data_prev_block[0], 'amount': data_prev_block[1], 'to whom': data_prev_block[2], 'hash': data_prev_block[3]})
    return hashlib.sha256(data_to_json.encode("utf-8")).hexdigest(), data_prev_block[4]

def get_files() -> list:
    files = os.listdir(blockchain_dir)
    return sorted([int(i) for i in files])


def write_block(name, amount, to_whom, prev_hash=''):
    prev_index = 0
    if database.is_database_exist() == False:
        prev_hash, prev_index = get_hash_db()
    database.add_block(name, str(amount), to_whom, prev_hash, prev_index)



# def write_block(name, amount, to_whom, prev_hash=''):
#     files = get_files()
#     if len(files) == 0:
#         filename = "1"
#         prev_hash = None
#     else:
#         prev_file = files[-1]
#         filename = str(prev_file + 1)
#         prev_hash = get_hash(str(prev_file))

#     data = {'name': name, 'amount': amount,
#             'to whom': to_whom, 'hash': prev_hash}
#     with open(blockchain_dir + filename, 'w', encoding='utf-8') as file:
#         json.dump(data, file, indent=4, ensure_ascii=False)


def check_integrity():
    files = get_files()
    results = []
    for file in files[1:]:
        f = open(blockchain_dir + str(file))
        h = json.load(f)['hash']
        prev_file = str(file - 1)
        actual_hash = get_hash(prev_file)
        if h == actual_hash:
            res = 'ok'
        else:
            res = 'currepted'
        results.append({'block': prev_file, 'result': res})
    return results


# def main():
#     check_integrity()
#     write_block("Tema", 5, "Leha")


# if __name__ == '__main__':
#     print(get_hash_db())