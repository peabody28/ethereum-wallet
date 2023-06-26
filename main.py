from jsonrpcclient import request as rpc_req
from jsonrpcclient import parse_json as rpc_parse
from tkinter import *
from tkinter import ttk

import currencyHelper
import httpHelper
import configuration

approvingRequiredMessage = "For this action required manual approving in Clef console!"

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


def printApprovingRequiredMessage():
    print(approvingRequiredMessage)


def printMenu():
    print("--------------------------------------------")
    print("- wallets\n"
          "- wallet_balance\n"
          "- gas_price\n"
          "- wallet_transaction_count\n"
          "- send_transaction")


walletsList = []

def configureWalletsWindow(frame):
    global walletsList
    if len(walletsList) == 0:
        printApprovingRequiredMessage()
        walletsList = getWallets()

    for walletNumber in walletsList:
        block = Frame(master=frame)

        label = Entry(master=block, font=("Arial", 12), width=45)
        label.insert(END, walletNumber)
        label.pack(side=LEFT)
        label.config(state="readonly")

        balance = Entry(master=block, font=("Arial", 12))
        balance.insert(END, getBalance(walletNumber))
        balance.pack(side=RIGHT)
        balance.config(state="readonly")

        block.pack(fill=X, side=TOP)


def configureBlockchainInfoWindow(frame):
    gasPrice = getGasPrice()
    gasPriceLabel = ttk.Label(master=frame, text="Gas price")
    gasPriceLabel.pack(side=TOP)

    entry = Entry(master=frame, font=("Arial", 12), width=45)
    entry.insert(END, gasPrice)
    entry.pack(side=TOP)
    entry.config(state="readonly")

    commissionLabel = ttk.Label(master=frame, text="Commission")
    commissionLabel.pack(side=TOP)

    commission = Entry(master=frame, font=("Arial", 12), width=45)
    commission.insert(END, gasPrice * 21000)
    commission.pack(side=TOP)
    commission.config(state="readonly")


def sendTransacionButtonHandler(walletFromEntry, walletToEnty, amountEntry, message):
    response = sendTransaction(walletFromEntry.get(), walletToEnty.get(), float(amountEntry.get()))

    message.config(state="normal")
    message.delete(0, END)
    message.insert(END, response)
    message.config(state="readonly")


def configureTransactionsTab(frame):
    labelFrom = ttk.Label(master=frame, text="Wallet from")
    labelFrom.pack(side=TOP)
    walletFrom = Entry(master=frame, font=("Arial", 12), width=45)
    walletFrom.pack(side=TOP)

    labelFrom = ttk.Label(master=frame, text="Wallet to")
    labelFrom.pack()
    walletTo = Entry(master=frame, font=("Arial", 12), width=45)
    walletTo.pack(side=TOP)

    labelAmount = ttk.Label(master=frame, text="Amount")
    labelAmount.pack()
    amount = Entry(master=frame, font=("Arial", 12), width=20)
    amount.pack(side=TOP, pady=(0, 5))

    message = ttk.Entry(master=frame)
    message.insert(END, approvingRequiredMessage)

    button = ttk.Button(master=frame, text="Send", command=lambda: sendTransacionButtonHandler(walletFrom, walletTo, amount, message))
    button.pack(side=TOP)

    message.pack(side=TOP, fill=X, pady=(5, 0))
    message.config(state="readonly")

root = Tk()
root.title("Ethereum local wallet")
root.geometry("650x400")

notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH)

wallets = ttk.Frame(notebook)
blockChainInfo = ttk.Frame(notebook)
sendTransactionTab = ttk.Frame(notebook)

wallets.pack(fill=BOTH, expand=True)
blockChainInfo.pack(fill=BOTH, expand=True)
sendTransactionTab.pack(fill=BOTH, expand=True)

notebook.add(wallets, text="Wallets")
notebook.add(blockChainInfo, text="Blockchain Info")
notebook.add(sendTransactionTab, text="Transactions")

configureWalletsWindow(wallets)
configureBlockchainInfoWindow(blockChainInfo)
configureTransactionsTab(sendTransactionTab)

root.mainloop()

# 0xEd44F8f248D1aA634bCCfEF02AC6c13e673d68e1
# 0x79d00246f60d58e955754b8e0cd8b584d6e7e875