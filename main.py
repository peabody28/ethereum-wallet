from jsonrpcclient import request as rpc_req
from jsonrpcclient import parse_json as rpc_parse

import currencyHelper
import httpHelper
import configuration


def getBalance(wallet):
    req = rpc_req(configuration.methods["getBalanceMethod"], [wallet, "latest"])
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
    gasPrice = getGasPrice()
    weiGas = currencyHelper.toWei(gasPrice)

    req_obj = {'from': walletFrom, 'to': walletTo, 'value': hex(weiAmount), 'gas': hex(weiGas), 'gasPrice': hex(weiGas)}
    req = rpc_req(configuration.methods["sendTransaction"], [req_obj])

    response = httpHelper.sendRequest(configuration.gethRpcApi, req)

    data = rpc_parse(response.content)
    return data.message


def signTransaction(txObject):
    req = rpc_req("account_signTransaction", [txObject])

    response = httpHelper.sendRequest(configuration.clefRpcApi, req)

    data = rpc_parse(response.content)
    return data.result


def printMenu():
    print("--------------------------------------------")
    print("- wallet_balance\n"
          "- gas_price\n"
          "- wallet_transaction_count\n"
          "- send_transaction")


while True:
    printMenu()
    actionCode = input()

    if(actionCode == "wallet_balance"):
        walletNumber = input("wallet number: ")
        print(getBalance(walletNumber))

    elif(actionCode == "gas_price"):
        print(getGasPrice())

    elif(actionCode == "wallet_transaction_count"):
        walletNumber = input("wallet number: ")
        print(getTransactionsCount(walletNumber))

    elif (actionCode == "send_transaction"):
        walletFrom = input("wallet from number: ")
        walletTo = input("wallet to number: ")
        amount = float(input("amount:"))

        response = sendTransaction(walletFrom, walletTo, amount)
        print(response)
    else:
        print("Bye!")
        break

# 0xEd44F8f248D1aA634bCCfEF02AC6c13e673d68e1 metamask
# 0x79d00246f60d58e955754b8e0cd8b584d6e7e875 geth