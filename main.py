from web3 import Web3
from utils import logger
import sys
import os 
from web3_functions import *

# Exe mode or python main.py mode
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
logger.info('[+] CWD: ' + os.getcwd())



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
            ftm_balance, usdc_balance, dai_balance =  check_balance(a)
            logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
            

    if choice == 2: 
        logger.info("Auto Swap started.")
        delay = 10 # delay between transactions
        
        for i in range(0, len(accounts)-1):

            a = accounts[i]
            b = accounts[i+1]
            ftm_balance, usdc_balance, dai_balance =  check_balance(a)
            logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
            
            # approve 
            approve_usdc(a) # B2
            time.sleep(delay)
            approve_dai(a) # B3
            time.sleep(delay)

            # swap usdc to dai
            swap_usdc_to_dai_1010u(a) # B4
            time.sleep(delay)

            # check balance again an swap back
            ftm_balance, usdc_balance, dai_balance =  check_balance(a) 
            swap_dai_to_usdc_1010u(a) # B5
            time.sleep(delay)

            # check balance
            ftm_balance, usdc_balance, dai_balance =  check_balance(a)
            logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))

            # send to next account
            transfer_all(a, b) # B6 7 8
            time.sleep(delay)

            ftm_balance, usdc_balance, dai_balance =  check_balance(a)

        logger.info("COMPLETED AUTO")

    if choice == 3:
        logger.info("Contact Telegram: @pycharmm to use this feature.")
    if choice == 4:
        logger.info("Author: quocmanh.pro | Telegram: @pycharmm")
