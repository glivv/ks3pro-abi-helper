from common import *
import requests
import json

contracts = load_contracts()

try:
    for chainId in chains:
        chainName = chains[chainId]['dir']

        if chainId not in contracts:
            contracts[chainId] = dict()

        for address in addresses:
            print(f'\r{chainName}/{address}', end='')

            url = f'{API_URL}chainid={chainId}&module=account&action=txlist&address={address}&startblock={chains[chainId]["start"]}&endblock={chains[chainId]["end"]}&page=1&offset=10000&sort=asc&apikey={API_KEY}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data['message'] == 'OK':
                    for tx in data['result']:
                        toAddr = tx['to'].lower()
                        if toAddr not in contracts[chainId] and len(tx['functionName']) > 0 and int(tx['gasUsed']) > 22000:
                            contracts[chainId][toAddr] = { 'contractName':'', 'implementation':'', 'name':'', 'symbol':'' }
                            print(f'\rcontract {chainName}/{toAddr} added')
                else:
                    print(f'\rno transactions for {chainName}/{address}')
            else:
                print(f'\rno response for {chainName}/{address}: {response.status_code}')
except Exception as ex:
    print(f'Exception "{ex}" while processing {chainName}/{address}')
finally:
    save_contracts(contracts)
