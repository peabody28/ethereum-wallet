import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# api url
gethRpcApi = config.get('RpcApiUrl', 'geth')
clefRpcApi = config.get('RpcApiUrl', 'clef')

# endpoints
# geth
methods = {
    'getBalanceMethod': config.get('RpcGethEndpoint', 'getBalance'),
    'getGasPrice': config.get('RpcGethEndpoint', 'getGasPrice'),
    'getBalance': config.get('RpcGethEndpoint', 'getBalance'),
    'getWalletTransactionsCount': config.get("RpcGethEndpoint", 'getWalletTransactionsCount'),
    'sendTransaction': config.get("RpcGethEndpoint", 'sendTransaction'),
    'wallets': config.get("RpcClefEndpoint", 'getWallets'),
}