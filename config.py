# get free api key at https://etherscan.io/apis
# manage your api keys at https://etherscan.io/apidashboard
API_KEY = 'your-etherscan-api-key'

# list of availble chains: https://docs.etherscan.io/etherscan-v2/getting-started/supported-chains
# list of rpcs: https://chainlist.org/
chains = {
    '1':{'start':0, 'end':'latest', 'dir':'ethereum', 'rpc':'https://rpc.mevblocker.io'},
    '10':{'start':0, 'end':'latest', 'dir':'optimism', 'rpc':'https://optimism-rpc.publicnode.com'},
    '137':{'start':0, 'end':'latest', 'dir':'polygon', 'rpc':'https://polygon-bor-rpc.publicnode.com'},
    '146':{'start':0, 'end':'latest', 'dir':'sonic', 'rpc':'https://rpc.soniclabs.com'},
    '252':{'start':0, 'end':'latest', 'dir':'fraxtal', 'rpc':'https://fraxtal-rpc.publicnode.com'},
    '42161':{'start':0, 'end':'latest', 'dir':'arbitrum', 'rpc':'https://arb1.arbitrum.io/rpc'},
    '43114':{'start':0, 'end':'latest', 'dir':'avalanche', 'rpc':'https://avalanche-c-chain-rpc.publicnode.com'},
    '56':{'start':0, 'end':'latest', 'dir':'bsc', 'rpc':'https://bsc.blockrazor.xyz'},
    '80094':{'start':0, 'end':'latest', 'dir':'berachain', 'rpc':'https://rpc.berachain-apis.com'},
    '8453':{'start':0, 'end':'latest', 'dir':'base', 'rpc':'https://base-rpc.publicnode.com'},
}

addresses = [
    #'0x32d03db62e464c9168e41028ffa6e9a05d8c6451','0x425d16b0e08a28a3ff9e4404ae99d78c0a076c5a',
    #'0x7a16ff8270133f063aab6c9977183d9e72835428','0x9b44473e223f8a3c047ad86f387b80402536b029',
    #'0xf89501b77b2fa6329f94f5a05fe84cebb5c8b1a0','0xC1671c9efc9A2ecC347238BeA054Fc6d1c6c28F9',

    #'0x4452b58d2fdb19dc757085ef6200a5ff549fbda9','0xe4a5b241f97a328e36556e05d28a95c02a57214a',

    #'0xd360ecb91406717ad13c4fae757b69b417e2af6b',
]
