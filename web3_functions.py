from web3 import Web3
from dotenv import load_dotenv
import os 
import json 
import time
from utils import logger
import sys
import requests

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

def swap_krystal_custom(account,src, dest, srcAmount, minDestAmount, extraArgs):
    """Use smart swap router to swap custom amount, custom token"""
    SmartWalletProxy= w3.to_checksum_address('0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a')
    src_address = w3.to_checksum_address(src)
    dest_address = w3.to_checksum_address(dest)
    smartrouter_abi= json.load(open('input/smartrouter.abi.json','r'))
    smartrouter_contract= w3.eth.contract(address=SmartWalletProxy,abi=smartrouter_abi)
    nonce = w3.eth.get_transaction_count(account.address)
    
    params=(
        w3.to_checksum_address('0x864F01c5E46b0712643B956BcA607bF883e0dbC5'),
        srcAmount,
        minDestAmount,
        (src_address,dest_address),
        0,
        0,
        w3.to_checksum_address('0x168E4c3AC8d89B00958B6bE6400B066f0347DDc9'),
        extraArgs
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
        logger.info(f"Swap DAI<->USDC success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
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

def transfer_token(from_account, to_account, token_name, amount_in_wei, nonce=-1):
    """Transfer FTM or USDC to next wallet"""
    usdc_address = "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75"
    dai_address = w3.to_checksum_address('0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E')
    approve_abi = json.load(open('input/usdc.abi.json','r'))
    contract_usdc = w3.eth.contract(address=usdc_address,abi=approve_abi) 
    contract_dai = w3.eth.contract(address=dai_address,abi=approve_abi) 
    if nonce == -1:
        nonce =  w3.eth.get_transaction_count(from_account.address)
    
    if token_name == "usdc":
        send_tx = contract_usdc.functions.transfer(to_account.address, amount_in_wei).build_transaction({
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

    if token_name == "dai":
        send_tx = contract_dai.functions.transfer(to_account.address, amount_in_wei).build_transaction({
            'from': from_account.address,
            'gasPrice': w3.to_wei(500,'gwei'),
            'nonce': nonce,
            'gas': 300000
        })

        signed_txn = w3.eth.account.sign_transaction(send_tx, from_account.key)

        try: 
            tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.info(f"Transfer DAI success: https://ftmscan.com/tx/{w3.to_hex(tx)}")
        except Exception as e:
            logger.info(e) 
        
def build_tx(user_address, src, destination, srcAmount, minDestAmount):
    """Build transaction Krystal request
    return: ExtraArgs"""
    # user_address="0x277cc8233544f2689b8adcd2a763195dc713f18a"
    # destination="0x04068da6c83afcfa0e13ba15a6696662335d5b75"
    # src="0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e"
    platformWallet="0x168E4c3AC8d89B00958B6bE6400B066f0347DDc9"
    # srcAmount="1000000000000000000"
    # minDestAmount="549702"
    hint="0x5b7b226964223a224b72797374616c20536d61727453776170222c2273706c697456616c7565223a31303030307d5d"
    gasPrice="0"
    url = "https://api.krystal.app/fantom/v2/swap/buildTx?userAddress={}&dest={}&src={}&platformWallet={}&srcAmount={}&minDestAmount={}&hint={}&gasPrice={}&nonce=1".format(
        user_address,
        destination,
        src,
        platformWallet,
        srcAmount,
        minDestAmount,
        hint,
        gasPrice,
    )

    r = requests.get(url)
    rjs = json.loads(r.text)
    return rjs['txObject']['data']

def swap_usdc_to_dai_1010u(account):
    """Swap 1010 usdc to dai"""
    """Use smart swap router to swap""" 
    # configs informations
    userAddress=account.address.lower() # account owner
    src="0x04068DA6C83AFCFA0e13ba15A6696662335D5B75".lower() # swap to this token dai
    dest="0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E".lower() # swap from this token usdc
    
    srcAmount=int(1*10**6)   # swap amount input
    minDestAmount=int(srcAmount*10**12*0.9) # 90% sliprate
    extraArgs = build_tx(user_address=userAddress,src=src, destination=dest, srcAmount=srcAmount,minDestAmount=minDestAmount)
    extraArgs = "0x" + extraArgs[842:]
    # send txs
    swap_krystal_custom(account=account, src=src, dest=dest, srcAmount=srcAmount, minDestAmount=minDestAmount, extraArgs=extraArgs)

def swap_dai_to_usdc_1010u(account):
    """Swap 1010 dai to usdc"""
    """Use smart swap router to swap""" 
    # configs informations
    userAddress=account.address.lower() # account owner
    
    src="0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E".lower() # swap to this token
    dest="0x04068DA6C83AFCFA0e13ba15A6696662335D5B75".lower() # swap from this token
    
    srcAmount=int(1*10**18)   # swap amount input
    minDestAmount=int(srcAmount/10**12*0.9) # 90% sliprate
    extraArgs = build_tx(user_address=userAddress,src=src, destination=dest, srcAmount=srcAmount,minDestAmount=minDestAmount)
    extraArgs = "0x" + extraArgs[842:]
    # send txs
    swap_krystal_custom(account=account, src=src, dest=dest, srcAmount=srcAmount, minDestAmount=minDestAmount, extraArgs=extraArgs)

def transfer_all(a, b):
    """Transfer all tokens from account a to account b"""
    logger.info("Transfer all token from {} to {}".format(a.address,b.address))
    ftm_balance, usdc_balance, dai_balance =  check_balance(a)
    logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
    if not usdc_balance/10**6 <0.1 : 
        transfer_token(a,b,'usdc',usdc_balance)
        time.sleep(10)
    else:
        logger.error("USDC balance too low")
    
    if not ftm_balance/10**18 < 0.1: 
        transfer_token(a,b,'dai',dai_balance)
        time.sleep(10)
    else:
        logger.error("DAI balance too low")

    if not ftm_balance/10**18 < 0.02:
        ftm_balance, usdc_balance, dai_balance =  check_balance(a)
        transfer_token(a,b,'ftm',ftm_balance)
        time.sleep(10)
    else:
        logger.error("FTM balance too low")

    ftm_balance, usdc_balance, dai_balance =  check_balance(a)
    logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
    logger.info("Tranfer all success")
