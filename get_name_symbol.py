from common import *
from pathlib import Path
import requests
import json
from web3 import Web3

w3s = dict()

def getContract(chainId, addr, abi):
    global w3s

    if chainId not in w3s:
        w3s[chainId] = Web3(Web3.HTTPProvider(chains[chainId]['rpc']))

    return w3s[chainId].eth.contract(address=Web3.to_checksum_address(addr), abi=abi)


contracts = load_contracts()

abidir = Path('abi')
abidir.mkdir(parents=True, exist_ok=True)

try:
    for chainId in contracts:
        chainName = chains[chainId]['dir']

        for cAddress in contracts[chainId]:
            if len(contracts[chainId][cAddress]['name']) == 0 or len(contracts[chainId][cAddress]['symbol']) == 0:
                abi = None

                abifile = abidir / f'{chainId}-{cAddress}'
                if Path(abifile).is_file():
                    abi = Path(abifile).read_text()

                if not abi:
                    impAddr = contracts[chainId][cAddress]['implementation']
                    abiAddress = impAddr if len(impAddr) > 0 else cAddress

                    url = f'{API_URL}chainid={chainId}&module=contract&action=getabi&address={abiAddress}&apikey={API_KEY}'
                    response = requests.get(url)

                    if response.status_code == 200:
                        data = response.json()
                        if 'result' in data and 'not verified' not in data['result']:
                            abi = data['result']
                            Path(abifile).write_text(abi)
                            print(f'{chainName}/{cAddress}: downloaded abi')
                        else:
                            print(f'no abi for {chainName}/{cAddress}')
                    else:
                        print(f'no response for {chainName}/{cAddress}: {response.status_code}')

                if abi:
                    for item in json.loads(abi):
                        if item['type'] == 'function' and len(item['inputs']) == 0:
                            if item['name'] in ['name','symbol']:
                                web3c = getContract(chainId, cAddress, abi)
                                res = web3c.get_function_by_name(item['name'])().call()
                                if not isinstance(res, str):
                                    res = res.decode()

                                if len(res) > 0:
                                    contracts[chainId][cAddress][item['name']] = res
                                    print(f'{chainName}/{cAddress}: "{item["name"]}" set to {res}')
except Exception as ex:
    print(f'Exception "{ex}" while processing {chainName}/{cAddress}')
finally:
    save_contracts(contracts)
