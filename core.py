from jsonrpcclient import request as rpc_req
from jsonrpcclient import parse_json as rpc_parse

import currencyHelper
import httpHelper
import configuration


def getBalance(wallet):
    req = rpc_req(configuration.methods["getBalance"], [wallet, "latest"])
    response = httpHelper.sendRequest(configuration.gethRpcApi, req)

    data = rpc_parse(response.content)
    amount = int(data.result, 16)

    return currencyHelper.toEther(amount)


def getGasPrice():
    req = rpc_req(configuration.methods["getGasPrice"])
    response = httpHelper.sendRequest(configuration.gethRpcApi, req)

    data = rpc_parse(response.content)
    amount = int(data.result, 16)

    return currencyHelper.toEther(amount)


# integer of the number of transactions send from this address.
def getTransactionsCount(wallet):
    req = rpc_req(configuration.methods["getWalletTransactionsCount"], [wallet, "latest"])
    response = httpHelper.sendRequest(configuration.gethRpcApi, req)

    data = rpc_parse(response.content)
    count = int(data.result, 16)

    return count


def sendTransaction(walletFrom, walletTo, ethAmount):
    weiAmount = currencyHelper.toWei(ethAmount)

    req_obj = {'from': walletFrom, 'to': walletTo, 'value': hex(weiAmount)}
    req = rpc_req(configuration.methods["sendTransaction"], [req_obj])

    response = httpHelper.sendRequest(configuration.gethRpcApi, req)

    data = rpc_parse(response.content)
    return data.result if response.status_code == 200 else data.message


def getWallets():
    req = rpc_req(configuration.methods["wallets"])
    response = httpHelper.sendRequest(configuration.clefRpcApi, req)

    data = rpc_parse(response.content)

    return data.result
