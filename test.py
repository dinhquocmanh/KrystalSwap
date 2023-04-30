from main import *

if __name__ == "__main__":
    accounts = read_input()
    logger.info('[+] Loaded total: {} accounts'.format(len(accounts))) 
    
    a = accounts[0]
    b = accounts[1]
    
    # ftm_balance, usdc_balance, dai_balance =  check_balance(a)
    # logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(a.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
    
    #ftm_balance, usdc_balance, dai_balance =  check_balance(b)
    #logger.info("Address: {} | FTM balance: {} | USDC balance: {} | DAI balance: {}".format(b.address, ftm_balance/10**18, usdc_balance/10**6, dai_balance/10**18))
    #transfer_token(a, b, 'usdc', usdc_balance)
    #transfer_token(a, b, 'ftm', ftm_balance)
    transfer_all(b,a)
    #swap_dai_to_usdc_1u(a)
    #time.sleep(7)
    # swap_dai_to_usdc_1010u(b)
    # time.sleep(7)
    # swap_usdc_to_dai_1010u(b)
    # time.sleep(7)


    # configs informations
    userAddress=b.address.lower() # account owner
    dest="0x04068DA6C83AFCFA0e13ba15A6696662335D5B75".lower() # swap from this token
    src="0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E".lower() # swap to this token
    srcAmount=int(0.01*10**18)   # swap amount input
    minDestAmount=int(srcAmount/10**12*0.9) # 90% sliprate
    extraArgs = build_tx(user_address=userAddress,src=src, destination=dest, srcAmount=srcAmount,minDestAmount=minDestAmount)
    extraArgs = "0x" + extraArgs[842:]
    #print(extraArgs)
    # send txs
    #swap_krystal_custom(account=b, src=src, dest=dest, srcAmount=srcAmount, minDestAmount=minDestAmount, extraArgs=extraArgs)