from config import *
import os
import datetime
import json
from pathlib import Path

API_URL = 'https://api.etherscan.io/v2/api?'
CONTRACTS_FILE = 'contracts.json'

addresses = list(a.lower() for a in addresses)

def load_contracts():
    if Path(CONTRACTS_FILE).is_file():
        with open(CONTRACTS_FILE, 'r') as file:
            return json.load(file)

    return dict()

def save_contracts(cdict, backup=True):
    if backup:
        if Path(CONTRACTS_FILE).is_file():
            os.rename(CONTRACTS_FILE, f'{CONTRACTS_FILE}_{datetime.datetime.now():%Y%m%d-%H%M%S}')

    with open(CONTRACTS_FILE, 'w') as c_file:
        json.dump(cdict, c_file, indent=4)
