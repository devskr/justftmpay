# This is polygon token and coin api to know how to use dm @ChauhanDev07 on telegram 

from flask import Flask, request, jsonify
import json
from web3 import Web3,HTTPProvider
from web3.middleware import geth_poa, geth_poa_middleware
from eth_account import Account

app = Flask(__name__)

# Connect to the FTM network
w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/fantom/"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"}]')


@app.route("/token", methods=['GET'])
def send_tokens():
    try:
         recipient_address = Web3.toChecksumAddress(request.args.get("receiver"))
         amount = request.args.get("amount")
         MY_PRIVATE_KEY = request.args.get("privatekey")
         contract = request.args.get("contract")
         TOKEN_ADDRESS = Web3.toChecksumAddress(contract)
         PA = w3.eth.account.from_key(MY_PRIVATE_KEY)
         MY_ADDRESS = Web3.toChecksumAddress(PA.address)
         token_contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=abi)
         nonce = w3.eth.getTransactionCount(MY_ADDRESS)
         gas_amount = token_contract.functions.transfer(recipient_address, w3.toWei(amount, "ether")).estimateGas({"from": MY_ADDRESS})
         gas_price = w3.eth.gasPrice
         contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=abi)
         totalSupply = contract.functions.totalSupply().call()
         amo = w3.toWei(amount, 'ether')
         tx = contract.functions.transfer(recipient_address, amo).buildTransaction({
             'chainId':250, 
             'gas': gas_amount,
             'gasPrice': gas_price,
             'nonce':nonce})
         sign_tx = w3.eth.account.signTransaction(tx, MY_PRIVATE_KEY)
         tran_hash = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
         txn = w3.toHex(tran_hash)
         return txn
    except Exception as e:
        return '{ "status": "error", "message": "'+str(e)+'"}'


@app.route("/wallet", methods=["GET"])
def create_wallet():
    private_key, address = w3.eth.account.create().privateKey, w3.eth.account.create().address
    return jsonify({"address": address, "privateKey": private_key.hex()})


@app.route('/coin', methods = ['GET'])
def send_coin():
    try:
        index = request.args.get
        address = index("receiver")
        amount = index("amount")
        privateKey = index("privatekey")
        PA = w3.eth.account.from_key(privateKey)
        saddress = Web3.toChecksumAddress(PA.address)
        value = amount
        to = address
        nonce = w3.eth.getTransactionCount(saddress)
        amo = w3.toWei(value, 'ether')
        gas_price = w3.eth.gasPrice
        tx = {'nonce' : nonce,'to' : to,'value' : amo, 'chainId':250, 'gas' : 21000,'gasPrice' : gas_price}
        sign_tx = w3.eth.account.signTransaction(tx, privateKey)
        tran_hash = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
        txn = w3.toHex(tran_hash)
        return txn
    except Exception as e:
        return '{ "status": "error", "message": "'+str(e)+'"}'


@app.route('/')
def setuphandler():
 return ("This is polygon token and coin api to know how to use dm @ChauhanDev07 on telegram ")
