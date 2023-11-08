from statistics import mean
import time
from web3 import Web3
import requests
import random
from datetime import datetime
import config
import contracts
import fun
from fun import *

deploy_abi = []

keys_list = []
with open("private_keys.txt", "r") as f:
    for row in f:
        private_key=row.strip()
        if private_key:
            keys_list.append(private_key)

i=0
for private_key in keys_list:
    i+=1

    try:
        web3 = Web3(Web3.HTTPProvider(config.rpc_links['scroll'], request_kwargs=config.request_kwargs))
        account = web3.eth.account.from_key(private_key)
        wallet = account.address    
        log(f"I-{i}: Начинаю работу с {wallet}")
        balance = web3.eth.get_balance(wallet)
        balance_decimal = Web3.from_wei(balance, 'ether')        

        if balance_decimal < config.minimal_need_balance:
            log("Недостаточно эфира")
            continue 

        mainnet = Web3(Web3.HTTPProvider(config.rpc_links['ETH']))
        while True:
            gasPrice = mainnet.eth.gas_price
            gasPrice_Gwei = Web3.from_wei(gasPrice, 'Gwei')
            log(f"gasPrice_Gwei = {gasPrice_Gwei}")
            if config.max_gas_price > gasPrice_Gwei:
                break
            else:
                log("Жду снижения цены за газ")
                timeOut()

        contract = web3.eth.contract(
            abi=deploy_abi,
            bytecode=random.choice(contracts.deploy_bytecode)
        )

        transaction = contract.constructor().build_transaction({
            'from': wallet,
            'value': 0,
            "gasPrice": web3.eth.gas_price ,
            'nonce': web3.eth.get_transaction_count(wallet),
        })
        gasLimit = web3.eth.estimate_gas(transaction)
        transaction['gas'] = int(gasLimit * config.gas_kef)

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        txn_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
        tx_result = web3.eth.wait_for_transaction_receipt(txn_hash)

        if tx_result['status'] == 1:
            contractAddress = tx_result['contractAddress']
            log_ok(f'deploy OK: https://scrollscan.com/tx/{txn_hash}')
            log_ok(f'contractAddress: {contractAddress}')
        else:
            log_error(f'deploy false: {txn_hash}')

        timeOut()
    
    except Exception as error:
        fun.log_error(f'Error: {error}')    
        timeOut("teh")
        continue
    
log("Ну типа все, кошельки закончились!")        

