from common import *
from pathlib import Path
import requests
import json

contracts = load_contracts()

abidir = Path('abi')
abidir.mkdir(parents=True, exist_ok=True)

for chainId in contracts:
    chainName = chains[chainId]['dir']

    ksabidir = Path('ks-abi') / chainName
    Path(ksabidir).mkdir(parents=True, exist_ok=True)

    for cAddress in contracts[chainId]:
        if len(contracts[chainId][cAddress]['contractName']) > 0:
            ksabifile = ksabidir / f'{cAddress}.json'

            if not Path(ksabifile).is_file():
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
                            print(f'{chainName}/{cAddress}: no abi')
                    else:
                        print(f'{chainName}/{cAddress}: no response - {response.status_code}')

                if abi:
                    ksabi = dict()
                    if len(contracts[chainId][cAddress]['name']) > 0:
                        if len(contracts[chainId][cAddress]['symbol']) > 0:
                            ksabi['name'] = f"{contracts[chainId][cAddress]['name']} ({contracts[chainId][cAddress]['symbol']})"
                        else:
                            ksabi['name'] = contracts[chainId][cAddress]['name']
                    elif len(contracts[chainId][cAddress]['symbol']) > 0:
                        ksabi['name'] = contracts[chainId][cAddress]['symbol']
                    else:
                        ksabi['name'] = contracts[chainId][cAddress]['contractName']
                    ksabi['chainId'] = chainId
                    ksabi['address'] = cAddress
                    ksabi['metadata'] = dict()
                    ksabi['metadata']['output'] = dict()
                    ksabi['metadata']['output']['abi'] = json.loads(abi)
                    ksabi['metadata']['output']['userdoc'] = list()
                    ksabi['metadata']['output']['devdoc'] = list()
                    ksabi['version'] = 1
                    ksabi['checkPoints'] = list()
                    ksabi['isProxy'] = len(contracts[chainId][cAddress]['implementation']) > 0
                    ksabi['principalAddress'] = contracts[chainId][cAddress]['implementation']

                    with open(ksabifile, 'w') as f:
                        json.dump(ksabi, f, indent=4)

                    print(f'{chainName}/{cAddress}: saved {ksabifile}')
