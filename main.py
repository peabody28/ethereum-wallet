from tkinter import *
from tkinter import ttk

import core

approvingRequiredMessage = "For this action required manual approving in Clef console!"

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
        walletsList = core.getWallets()

    for walletNumber in walletsList:
        block = Frame(master=frame)

        label = Entry(master=block, font=("Arial", 12), width=45)
        label.insert(END, walletNumber)
        label.pack(side=LEFT)
        label.config(state="readonly")

        balance = Entry(master=block, font=("Arial", 12))
        balance.insert(END, core.getBalance(walletNumber))
        balance.pack(side=RIGHT)
        balance.config(state="readonly")

        block.pack(fill=X, side=TOP)


def configureBlockchainInfoWindow(frame):
    gasPrice = core.getGasPrice()
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
    response = core.sendTransaction(walletFromEntry.get(), walletToEnty.get(), float(amountEntry.get()))

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

    button = ttk.Button(master=frame, text="Send", command=lambda: sendTransacionButtonHandler(walletFrom, walletTo, amount, message))
    button.pack(side=TOP)

    message = ttk.Entry(master=frame)
    message.insert(END, approvingRequiredMessage)
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