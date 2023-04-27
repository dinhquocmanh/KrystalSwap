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

def swap_dai_to_usdc(account, amount_ftm_in_wei):
    """Swap dai to usdc use router sushiswap"""
    Sushiswapv2Router = w3.to_checksum_address('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506') 
    SmartWalletProxy= w3.to_checksum_address('0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a')
    MultichainUSDC= w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')
    DAI_TOKEN_ADDRESS=w3.to_checksum_address('0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E')

    smartrouter_abi= json.load(open('input/smartrouter.abi.json','r'))
    smartrouter_contract= w3.eth.contract(address=SmartWalletProxy,abi=smartrouter_abi)
    nonce = w3.eth.get_transaction_count(account.address)

    params=(
        w3.to_checksum_address('0x848c15AB2330285Bbe0740f11B97b2ac530FB881'),
        amount_ftm_in_wei,
        99194, # to be change
        (DAI_TOKEN_ADDRESS,w3.to_checksum_address('0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'),MultichainUSDC),
        0,
        0,
        w3.to_checksum_address('0x168E4c3AC8d89B00958B6bE6400B066f0347DDc9'),
        Sushiswapv2Router
    )


    tx = smartrouter_contract.functions.swap(params).build_transaction({
        'from': account.address,
        'gasPrice': w3.to_wei(500,'gwei'),
        'nonce': nonce,
        'gas': 500000,
        }
    )

    signed_txn = w3.eth.account.sign_transaction(tx, account.key)

    try: 
        tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Swap DAI->USDC success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
    except Exception as e:
        logger.info(e)

def swap_dai_to_usdc2(account, amount_ftm_in_wei):
    """Use smart swap router to swap"""
    Sushiswapv2Router = w3.to_checksum_address('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506') 
    SmartWalletProxy= w3.to_checksum_address('0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a')
    MultichainUSDC= w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')
    DAI_TOKEN_ADDRESS=w3.to_checksum_address('0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E')

    smartrouter_abi= json.load(open('input/smartrouter.abi.json','r'))
    smartrouter_contract= w3.eth.contract(address=SmartWalletProxy,abi=smartrouter_abi)
    nonce = w3.eth.get_transaction_count(account.address)

    params=(
        w3.to_checksum_address('0x864F01c5E46b0712643B956BcA607bF883e0dbC5'),
        1000000000000000000,
        994606, # to be change
        (DAI_TOKEN_ADDRESS,MultichainUSDC),
        0,
        0,
        w3.to_checksum_address('0x168E4c3AC8d89B00958B6bE6400B066f0347DDc9'),
        "0x8af033fb0000000000000000000000001d5702c6d7eb30e42a8c94b8db7ea2e8444a37fd0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000028000000000000000000000000000000000000000000000000000000000000006400000000000000000000000008d11ec38a3eb5e956b052f67da8bdc9bef8abf3e00000000000000000000000004068da6c83afcfa0e13ba15a6696662335d5b750000000000000000000000000000000000000000000000000000000000000160000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001a000000000000000000000000000000000000000000000000000000000000001c0000000000000000000000000277cc8233544f2689b8adcd2a763195dc713f18a0000000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000000000000000000000000cb66b000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000001e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003a0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000644a1b6600000000000000000000000000000000000000000000000000000000000003600000000000000000000000000000000000000000000000000000000000000001000000000000000000000000484237bc35ca671302d19694c66d617142fbc23500000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000de0b6b3a76400000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000001e00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000040d0796174000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000120000000000000000000000000484237bc35ca671302d19694c66d617142fbc2350000000000000000000000008d11ec38a3eb5e956b052f67da8bdc9bef8abf3e00000000000000000000000004068da6c83afcfa0e13ba15a6696662335d5b750000000000000000000000001d5702c6d7eb30e42a8c94b8db7ea2e8444a37fd00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000027100000000000000000000000000000000000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ee7b22536f75726365223a226b72797374616c222c22416d6f756e74496e555344223a22302e393939373731222c22416d6f756e744f7574555344223a22302e39393937353030303139333539393939222c22526566657272616c223a22222c22466c616773223a332c22496e74656772697479496e666f223a7b224b65794944223a2231222c225369676e6174757265223a2251505778766775354e714e373162395879705671664e63744b6f413554774657687a3273697343384b7868706a766576776979692f3343326f6d4449617a523737412f3252417a54635a356473726a39384763702f6f6e78414c307a442b4a58715847306c31537551587953624a4b4a52544c4f7a41436f4144745a62466f49496355334b486d2f31675159334268483669574d4f346e55394a46703138632f66414a545769495a42486c486d2f4d4849477561314548524c4a4865416d732b59412f52444f726b5a4672476e58474a4d326f78754a3147554d4f67424d6e326856304d73694e495534616e726b41412b68426658484b6f343166627558614379524e4b48485751393047537957676947424463475146474e727173572b38333668396b686b44445356647772674c3845627a354d64783345744c37474976466676437373666c697a5664377154442b4e38354f72673d3d227d7d000000000000000000000000000000000000"
    )


    tx = smartrouter_contract.functions.swap(params).build_transaction({
        'from': account.address,
        'gasPrice': w3.to_wei(500,'gwei'),
        'nonce': nonce,
        'gas': 500000,
        }
    )

    signed_txn = w3.eth.account.sign_transaction(tx, account.key)

    try: 
        tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Swap DAI->USDC success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
    except Exception as e:
        logger.info(e)

def swap_usdc_to_dai(account, amount_usdc_in_wei):
    # define
    Sushiswapv2Router = w3.to_checksum_address('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506') 
    SmartWalletProxy= w3.to_checksum_address('0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a')
    MultichainUSDC= w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')
    DAI_TOKEN_ADDRESS=w3.to_checksum_address('0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E')

    smartrouter_abi= json.load(open('input/smartrouter.abi.json','r'))
    smartrouter_contract= w3.eth.contract(address=SmartWalletProxy,abi=smartrouter_abi)
    nonce = w3.eth.get_transaction_count(account.address)

    params=(
        w3.to_checksum_address('0x848c15AB2330285Bbe0740f11B97b2ac530FB881'),
        amount_usdc_in_wei,
        98320556728354150, # to be change
        (MultichainUSDC,w3.to_checksum_address('0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'),w3.to_checksum_address('0x74b23882a30290451A17c44f4F05243b6b58C76d'), DAI_TOKEN_ADDRESS),
        1,
        0,
        w3.to_checksum_address('0x168E4c3AC8d89B00958B6bE6400B066f0347DDc9'),
        Sushiswapv2Router
    )

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
        logger.info(f"Swap USDC->DAI success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
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
        logger.info(f"Approved USDC success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
    except Exception as e:
        logger.info(e)

def approve_dai(account):
    """Approve dai to trade on SmartWalletProxy
    # approve this address to spend my money"""
    max_unint256=115792089237316195423570985008687907853269984665640564039457584007913129639935
    DAI_TOKEN_ADDRESS= w3.to_checksum_address('0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E')
    SmartWalletProxy= w3.to_checksum_address('0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a')
    approve_abi = json.load(open('input/usdc.abi.json','r'))
    contract = w3.eth.contract(address=DAI_TOKEN_ADDRESS,abi=approve_abi) 
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
        logger.info(f"Approved DAI success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
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

    # dai
    dai_address= w3.to_checksum_address('0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E')
    dai_abi= json.load(open('input/usdc.abi.json','r'))
    dai_contract = w3.eth.contract(address=dai_address,abi=dai_abi)
    dai_balance = dai_contract.functions.balanceOf(account.address).call()

    return ftm_balance, usdc_balance, dai_balance

def transfer_token(from_account, to_account, token_name, amount_in_wei):
    """Transfer FTM or USDC to next wallet"""
    usdc_address = "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75"
    approve_abi = json.load(open('input/usdc.abi.json','r'))
    contract = w3.eth.contract(address=usdc_address,abi=approve_abi) 
    nonce =  w3.eth.get_transaction_count(from_account.address)
    
    if token_name == "usdc":
        send_tx = contract.functions.transfer(to_account.address, amount_in_wei).build_transaction({
            'from': from_account.address,
            'gasPrice': w3.to_wei(500,'gwei'),
            'nonce': nonce,
            'gas': 300000
        })

        signed_txn = w3.eth.account.sign_transaction(send_tx, from_account.key)

        try: 
            tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.info(f"Transfer USDC success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
        except Exception as e:
            logger.info(e)

    if token_name == "ftm":
        send_tx = {
            'from': from_account.address,
            'to': to_account.address,
            'gasPrice': w3.to_wei(300,'gwei'),
            'nonce': nonce,
            'gas': 100000,
            'value': amount_in_wei-100000*w3.to_wei(300,'gwei'),
            'chainId': 250
        }
        signed_txn = w3.eth.account.sign_transaction(send_tx, from_account.key)

        try: 
            tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.info(f"Transfer FTM success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
        except Exception as e:
            logger.info(e) 


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

    choice = input("SELECT OPTIONS:\n1. Check Balance of all accounts.\n2. Swap USDC->DAI DAI->USDC and send to next account.\n3. Send money from account 1 to all account in one transaction.\n4. Author\n-> Your choice: ")
    logger.debug("User select: {}".format(choice))
    # default send all the money
    # if choice == '2':
    #     a = input("FTM amount to swap: ")
    #     options['FTM_amount'] = float(a)
    #     confirm = input('Do you want to swap {} FTM -> USDC for all account and repeat all acc? Type: Y/N: '.format(options['FTM_amount']))
    #     if confirm.lower() == 'y':
    #         return choice, options
    #     else: 
    #         sys.exit()
    
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
    
    a = accounts[1]
    b = accounts[0]
    
    ftm_balance, usdc_balance, dai_balance =  check_balance(b)
    logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
    
    # test
    swap_dai_to_usdc2(b,2)

    # print(logo)
    # choice, options = user_input()

    
    # if choice == 1:
    #     for a in accounts:
    #         ftm_balance, usdc_balance, dai_balance =  check_balance(a)
    #         logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
            

    # if choice == 2: 
    #     logger.info("Auto Swap started.")
    #     delay = 7 # delay between transactions
        
    #     for i in range(0, len(accounts)-1):

    #         a = accounts[i]
    #         b = accounts[i+1]
    #         ftm_balance, usdc_balance, dai_balance =  check_balance(a)
    #         logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
            
    #         # approve 
    #         approve_usdc(a)
    #         time.sleep(delay)
    #         approve_dai(a)
    #         time.sleep(delay)

    #         # swap usdc to dai
    #         swap_usdc_to_dai(a, usdc_balance)
    #         time.sleep(delay)

    #         # check balance again an swap back
    #         ftm_balance, usdc_balance, dai_balance =  check_balance(a)
    #         swap_dai_to_usdc(a, dai_balance)
    #         time.sleep(delay)

    #         # check balance
    #         ftm_balance, usdc_balance, dai_balance =  check_balance(a)
    #         logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))

    #         # send to next account
    #         transfer_token(a, b, 'usdc', usdc_balance)
    #         time.sleep(delay)

    #         ftm_balance, usdc_balance, dai_balance =  check_balance(a)
    #         transfer_token(a, b, 'ftm', ftm_balance)
    #     logger.info("COMPLETED AUTO")

    # if choice == 3:
    #     logger.info("Contact Telegram: @pycharmm to use this feature.")
    # if choice == 4:
    #     logger.info("Author: quocmanh.pro | Telegram: @pycharmm")
