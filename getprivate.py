from web3 import Web3 

PHANTOM_HTTP_PROVIDER="https://methodical-shy-owl.fantom.discover.quiknode.pro/73b2a6b99d298bb935f359ae8091e11f1aaabdac/"
w3 = Web3(Web3.HTTPProvider(PHANTOM_HTTP_PROVIDER))
if w3.is_connected():
    print("[+] Connect to FANTOM network success.")


def get_account_by_seed(seed_phrase):
    w3.eth.account.enable_unaudited_hdwallet_features()
    account = w3.eth.account.from_mnemonic(seed_phrase, account_path="m/44'/60'/0'/0/0")
    return account

if __name__ == "__main__":
    account = get_account_by_seed("")
    print(account.address)
    key = account.key
    p = w3.eth.account._parsePrivateKey(key)
    print(p)