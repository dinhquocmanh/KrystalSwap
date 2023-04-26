from web3 import Web3
import json 
import time
from dotenv import load_dotenv
import os 
import logging
import sys

# LOGGER
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
logger.info("[+] Program Started.")
logger.info("[+] Logger Setup Success")

# Exe mode or python main.py mode
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
logger.info('[+] CWD: ' + os.getcwd())


# INIT
load_dotenv('input/config.env')
logger.info("[+] Load input/config.env success.")
PHANTOM_HTTP_PROVIDER=os.getenv('PHANTOM_HTTP_PROVIDER')
w3 = Web3(Web3.HTTPProvider(PHANTOM_HTTP_PROVIDER))
if w3.is_connected():
    logger.info("[+] Connect to FANTOM network success.")
else:
    logger.error("Connect to FANTOM network failed.")
    sys.exit()


# FUNCTIONS
def get_account_by_seed(seed_phrase):
    w3.eth.account.enable_unaudited_hdwallet_features()
    account = w3.eth.account.from_mnemonic(seed_phrase, account_path="m/44'/60'/0'/0/0")
    return account

def get_account_by_private(privatekey):
    account = w3.eth.account.from_key(privatekey)
    return account 

def swap_ftm_to_usdc(account, amount_ftm):
    # define
    Sushiswapv2Router = w3.to_checksum_address('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506') 
    SmartWalletProxy= w3.to_checksum_address('0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a')
    MultichainUSDC= w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')
    FTM_TOKEN_ADDRESS= w3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')

    smartrouter_abi= json.load(open('input/smartrouter.abi.json','r'))
    smartrouter_contract= w3.eth.contract(address=SmartWalletProxy,abi=smartrouter_abi)
    nonce = w3.eth.get_transaction_count(account.address)

    params=(
        w3.to_checksum_address('0x848c15AB2330285Bbe0740f11B97b2ac530FB881'),
        w3.to_wei(amount_ftm, 'ether'),
        131763, # to be change
        (FTM_TOKEN_ADDRESS,MultichainUSDC),
        0,
        0,
        w3.to_checksum_address('0x168E4c3AC8d89B00958B6bE6400B066f0347DDc9'),
        Sushiswapv2Router
    )
        # swapContract
        # srcAmount
        # minDestAmount
        # tradePath
        # feeMode
        # feeBps
        # platformWallet
        # extraArgs


    tx = smartrouter_contract.functions.swap(params).build_transaction({
        'from': account.address,
        'gasPrice': w3.to_wei(500,'gwei'),
        'nonce': nonce,
        'gas': 500000,
        'value' :  w3.to_wei(amount_ftm, 'ether'),
        }
    )

    signed_txn = w3.eth.account.sign_transaction(tx, account.key)

    try: 
        tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Swap success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
    except Exception as e:
        logger.info(e)


def swap_usdc_to_ftm(account, amount_usdc):
    # define
    Sushiswapv2Router = w3.to_checksum_address('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506') 
    SmartWalletProxy= w3.to_checksum_address('0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a')
    MultichainUSDC= w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')
    FTM_TOKEN_ADDRESS= w3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')

    smartrouter_abi= json.load(open('input/smartrouter.abi.json','r'))
    smartrouter_contract= w3.eth.contract(address=SmartWalletProxy,abi=smartrouter_abi)
    nonce = w3.eth.get_transaction_count(account.address)

    params=(
        w3.to_checksum_address('0x848c15AB2330285Bbe0740f11B97b2ac530FB881'),
        w3.to_wei(amount_usdc, 'mwei'),
        220296527242228370, # to be change
        (MultichainUSDC,FTM_TOKEN_ADDRESS),
        1,
        0,
        w3.to_checksum_address('0x168E4c3AC8d89B00958B6bE6400B066f0347DDc9'),
        Sushiswapv2Router
    )
        # swapContract
        # srcAmount
        # minDestAmount
        # tradePath
        # feeMode
        # feeBps
        # platformWallet
        # extraArgs


    tx = smartrouter_contract.functions.swap(params).build_transaction({
        'from': account.address,
        'gasPrice': w3.to_wei(500,'gwei'),
        'nonce': nonce,
        'gas': 500000,
        #'value' :  w3.to_wei(amount_usdc, 'get') # 10^6
        }
    )

    signed_txn = w3.eth.account.sign_transaction(tx, account.key)

    try: 
        tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Swap success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
    except Exception as e:
        logger.info(e) 

def approve_usdc(account):
    """Approve usdc to trade on SmartWalletProxy
    # approve this address to spend my money"""
    max_unint256=115792089237316195423570985008687907853269984665640564039457584007913129639935
    MultichainUSDC= w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')
    SmartWalletProxy= w3.to_checksum_address('0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a')
    approve_abi = json.load(open('input/usdc.abi.json','r'))
    contract = w3.eth.contract(address=MultichainUSDC,abi=approve_abi) 
    balance_to_approve = max_unint256
    nonce =  w3.eth.get_transaction_count(account.address)
    

    approve_tx = contract.functions.approve(SmartWalletProxy, balance_to_approve).build_transaction({
        'from': account.address,
        'gasPrice': w3.to_wei(500,'gwei'),
        'nonce': nonce,
        'gas': 300000
    })

    signed_txn = w3.eth.account.sign_transaction(approve_tx, account.key)

    try: 
        tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Approved success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
    except Exception as e:
        logger.info(e)

def check_balance(account):
    """check balance FTM and USDC of wallet
    return ftm, usdc"""
    # ftm
    ftm_balance= w3.eth.get_balance(account.address)

    # usdc
    usdc_address= w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')
    usdc_abi= json.load(open('input/usdc.abi.json','r'))
    usdc_contract = w3.eth.contract(address=usdc_address,abi=usdc_abi)
    usdc_balance = usdc_contract.functions.balanceOf(account.address).call()

    return ftm_balance, usdc_balance

def transfer_ftm(account):
    pass 

def read_input():
    """Load input file 
    return account objects"""
    accounts = []
    account_objects=[]

    with open('input/wallets.txt','r') as f: 
        data = f.read()
    for line in data.split('\n'):
        a = {
            'id': line.split('\t')[0],
            'seedphrase': line.split('\t')[1],
            'privatekey': line.split('\t')[2],
            'address' : line.split('\t')[3]
        }
        accounts.append(a)
    for a in accounts:
        a_obj = get_account_by_private(a['privatekey'])
        account_objects.append(a_obj)

    return account_objects 

def user_input():
    """read input from user selection
    return run mode"""
    
    options = {
        'FTM_amount' : 1,
        'Disperse_amount' : 0
    }

    choice = input("SELECT OPTIONS:\n1. Check Balance of all accounts.\n2. Swap FTM->USDC USDC->FTM and send to next account.\n3. Send money from account 1 to all account.\n4. Author\n-> Your choice: ")
    logger.debug("User select: {}".format(choice))
    if choice == '2':
        a = input("FTM amount to swap: ")
        options['FTM_amount'] = float(a)
        confirm = input('Do you want to swap {} FTM -> USDC for all account and repeat all acc? Type: Y/N: '.format(options['FTM_amount']))
        if confirm.lower() == 'y':
            return choice, options
        else: 
            sys.exit()
    
    return int(choice), options

# MAIN
logo="""                                               _                       
   __ _ _   _  ___   ___ _ __ ___   __ _ _ __ | |__    _ __  _ __ ___  
  / _` | | | |/ _ \ / __| '_ ` _ \ / _` | '_ \| '_ \  | '_ \| '__/ _ \ 
 | (_| | |_| | (_) | (__| | | | | | (_| | | | | | | |_| |_) | | | (_) |
  \__, |\__,_|\___/ \___|_| |_| |_|\__,_|_| |_|_| |_(_) .__/|_|  \___/ 
     |_|                                              |_|              
"""
if __name__ == "__main__":
    accounts = read_input()
    logger.info('[+] Loaded total: {} accounts'.format(len(accounts))) 
    
    print(logo)
    choice, options = user_input()

    if choice == 1:
        for a in accounts:
            ftm_balance, usdc_balance = check_balance(a)
            ftm_balance = ftm_balance/10**18
            usdc_balance = usdc_balance/10**6
            logger.info("Address: {} | FTM balance: {} | USDC balance: {}".format(a.address, ftm_balance, usdc_balance))

    if choice == 2: 
        logger.info("Auto Swap started. Amount {} FTM".format(options['FTM_amount']))
    if choice == 3:
        logger.info("Contact Telegram: @pycharmm to use this feature.")
    if choice == 4:
        logger.info("Author: quocmanh.pro | Telegram: @pycharmm")

    # #swap_ftm_to_usdc(a,4)
    # #approve_usdc(a)
    # #swap_usdc_to_ftm(a, 1)

    # ftm_balance, usdc_balance = check_balance(a)
    # ftm_balance = ftm_balance/10**18
    # usdc_balance = usdc_balance/10**6
    # logger.info("FTM balance: {} | USDC balance: {}".format(ftm_balance, usdc_balance))