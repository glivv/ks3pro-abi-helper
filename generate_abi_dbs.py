import os
import json
import sqlite3
import shutil
from Crypto.Hash import keccak
from tqdm import tqdm

CHAIN_ID_MAP = {
    "arbitrum": 42161,
    "avalanche": 43114,
    "base": 8453,
    "berachain": 80094,
    "bsc": 56,
    "celo": 42220,
    "ethereum": 1,
    "fantom": 250,
    "flare": 14,
    "fraxtal": 252,
    "harmony": 1666600000,
    "moonriver": 1285,
    "optimism": 10,
    "polygon": 137,
    "songbird": 19,
    "sonic": 146,
}

connection_pool = dict()

def create_db_table(path):
    conn = sqlite3.connect(path)
    conn.execute('PRAGMA temp_store = MEMORY')
    conn.execute('PRAGMA synchronous = OFF')
    cursor = conn.cursor()
    try:
        create_table = """create table contracts
                (
                    id INTEGER PRIMARY KEY NOT NULL,
                    address VARCHAR(50) NOT NULL,
                    name VARCHAR(50),
                    selectorId VARCHAR(50),
                    functionABI TEXT,
                    version INTEGER DEFAULT 1,
                    checkPoints text DEFAULT NULL
                )"""

        sql_create_address_index = "create index address_index on contracts(address)"
        cursor.execute(create_table)
        cursor.execute(sql_create_address_index)
    except:
        clean_table = "DELETE FROM contracts"
        cursor.execute(clean_table)

    cursor.close()
    conn.commit()
    conn.close()

def get_or_create_db_table(path):
    if not os.path.exists(path):
        create_db_table(path)
        conn = sqlite3.connect(path)
        conn.execute('PRAGMA temp_store = MEMORY')
        conn.execute('PRAGMA synchronous = OFF')
        connection_pool[path] = conn
        return conn
    else:
        return connection_pool[path]

def caclulate_selector_id(function_name_with_type):
    bytes_for_function = bytes(function_name_with_type, 'utf-8')
    sha = keccak.new(digest_bits=256)
    sha.update(bytes_for_function)
    return sha.hexdigest()[0:8]

def process_function_abi_object(func_obj):
    if(len(func_obj["inputs"])>0):
        type_list = [each['type'] for each in func_obj["inputs"]]
        return ','.join(type_list)
    else:
        return ""

def parse_contract_json(json_contract):
    abi_list = json_contract["metadata"]["output"]["abi"]

    abi_func_list = [ each for each in abi_list if each["type"] == "function"]
    functions = [];
    for each in abi_func_list:
        function_signature = f"{each['name']}({process_function_abi_object(each)})"
        selector = caclulate_selector_id(function_signature)
        functions.append({ 'abi': each, 'selector': selector })

    return functions

def get_contract_info(contract_path):
    with open(contract_path, 'r') as f:
        try:
            content = json.loads(f.read())
            content_address = content["address"].lower()
            contract_name = content["name"]
            contract_metadate = json.dumps(content["metadata"])
            contract_version = 1
            contract_checkPoints = json.dumps(content.get("checkPoints",[]))
            abi_details = parse_contract_json(content)
        except Exception as e:
            print(f"exception {e} while getting contract info from {contract_path}")
            raise e

    return content_address, contract_name, contract_metadate, contract_version, contract_checkPoints, abi_details

def merge_abis_to_sqlite(chain_name, db_target_path, contracts_path):
    
    if not os.path.exists(contracts_path):
        return None

    for file in tqdm(os.listdir(contracts_path), desc=chain_name, ncols=100, mininterval=1, unit="contract"):
        if file.endswith(".json"):
            path = os.path.join(db_target_path, f"{CHAIN_ID_MAP[chain_name]}_{file[2].lower()}_contracts.db")
            conn = get_or_create_db_table(path)
            cursor = conn.cursor()

            address, name, metabase, version, check_points, abi_details = get_contract_info(contract_path=os.path.join(contracts_path, file))

            batch = []
            for fun in abi_details:
                batch.append((address, name, fun['selector'], json.dumps(fun['abi']), version, check_points))

            sql_insert_info = "insert into contracts (address,name,selectorId,functionABI,version,checkPoints) values (?,?,?,?,?,?)"
            cursor.executemany(sql_insert_info, batch)

            cursor.close()
            conn.commit()

if __name__ == "__main__":
    targets = [ name for name in os.listdir('ks-abi') ]
    db_target_path = "contracts"

    if os.path.exists(db_target_path):
        shutil.rmtree(db_target_path, ignore_errors=True)
    if not os.path.exists(db_target_path):
        os.makedirs(db_target_path)

    for target in targets:
        merge_abis_to_sqlite(target, db_target_path, contracts_path=f"ks-abi/{target}/")
        [conn.close() for conn in connection_pool.values()]
