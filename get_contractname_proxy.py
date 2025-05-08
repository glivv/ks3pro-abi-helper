from common import *
import requests
import json

contracts = load_contracts()

try:
    for chainId in chains:
        chainName = chains[chainId]['dir']

        for cAddress in contracts[chainId]:
            if len(contracts[chainId][cAddress]['contractName']) == 0:

                url = f'{API_URL}chainid={chainId}&module=contract&action=getsourcecode&address={cAddress}&apikey={API_KEY}'
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    if data['message'] == 'OK':
                        contractName = data['result'][0]['ContractName']
                        if len(contractName) == 0:
                            contractName = '??? UNKNOWN ???'

                        impAddr = data['result'][0]['Implementation']
                        if len(impAddr) == 0 or impAddr == cAddress:
                            impAddr = ''

                        contracts[chainId][cAddress]['contractName'] = contractName
                        contracts[chainId][cAddress]['implementation'] = impAddr

                        if len(impAddr) > 0 and impAddr != cAddress:
                            print(f'{chainName}/{cAddress}: {contractName}, implementation at {impAddr}')
                        else:
                            print(f'{chainName}/{cAddress}: {contractName}')
                    else:
                        print(f'no data for {chainName}/{cAddress}: {data["result"]}')
                else:
                    print(f'no response for {chainName}/{cAddress}: {response.status_code}')
except Exception as ex:
    print(f'Exception "{ex}" while processing {chainName}/{cAddress}')
finally:
    save_contracts(contracts)
