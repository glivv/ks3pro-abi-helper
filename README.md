## 0\. Edit `config.py`

`API_KEY`: get your API key at [etherscan](https://etherscan.io/apis) and enter it here

`chains`: add/delete/comment/uncomment chains where you want transactions to be taken from

`addresses`: enter addresses which transactions are taken

## 1\. Run `get_contracts.py`

script cycles through chains+addresses in the `config.py` and saves addresses of interacted contracts to the `contracts.json`

each time `contracts.json` is saved existing `contracts.json` is backed up under `contracts.json_YYYYMMDD-HHMMSS` name

contracts addresses could be added manually to the `contracts.json`

## 2\. Run `get_contractname_proxy.py`

script cycles through contracts addresses in the `contracts.json`, gets contract name and implementation address (in case of proxy), and updates "contractName" and "implementation" fields in the `contracts.json`

in case no contract name is received from etherscan `??? UNKNOWN ???` is stored as a contract name, fix these cases manually if needed

## 3\. Run `get_name_symbol.py`

script cycles through contracts addresses in the `contracts.json`, calls contract's name() and symbol() methods if those are present (contract's ABI is downloaded in the process), and updates "name" and "symbol" fields in the `contracts.json`

downloaded ABIs are cached in the `abi` folder

## 4\. Run `get_abis.py`

script cycles through contracts addresses in the `contracts.json`, gets contracts ABIs and stores them using `generate_abi_dbs.py`'s format to the `*.json` files in the `ks-abi` folder

name of the contract is set to the "name (symbol)", "symbol", or "contractName" based on what is available in the `contracts.json`

[`*.json` files from the KeystoneHQ's Smart-Contract-Metadata-Registry](https://github.com/KeystoneHQ/Smart-Contract-Metadata-Registry/) could be added manually to the corresponding folders under `ks-abi` folder

downloaded ABIs are cached in the `abi` folder

## 5\. Run `generate_abi_dbs.py`

script cycles through `*.json` files in the `ks-abi` folder and writes `*.db` files to the `contracts` folder

`generate_abi_dbs.py` is [updated version](https://github.com/glivv/ks3pro-abi-helper/commit/935add7ece9d55a4cd88660b3cf8a3aa987a57a5) of the [KeystoneHQ's generate_abi_dbs.py](https://github.com/KeystoneHQ/Smart-Contract-Metadata-Registry/blob/main/v3/generate_abi_dbs.py)

`contracts` folder is [final result](https://guide.keyst.one/docs/abi), copy it to the root of the SD card
