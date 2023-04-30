# Krystal Swap token 
Author: quocmanh

yêu cầu là: swap trên sàn dex krystal như t gửi ở trên. các tính năng gồm: 
set vol swap, 
set chuyển usdc (dai) sang ví tiếp theo sau khi swap + gas , 
set số lệnh swap/1 ví, chọn mặc định router

https://defi.krystal.app/swap?chainId=56
https://www.plexus.app/

Transactions
Swap FTM-> USDC: https://ftmscan.com/tx/0xbd84d8874c61bc0bf016cbe97ae56be98782e0c3d5a065abbea80ed4a349aeea
Approve USDC: https://ftmscan.com/tx/0x6111b66c9f476e0d67d8018ef75c308e808f74a77093708f51380c11a21cba47
Swap USDC-> FTM: https://ftmscan.com/tx/0x775e3b745ffd1089b5b27403af73e8b1f18021e7d09cb6954c7f524e7a968454


Address Phantom network
Sushiswapv2Router: 0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506
SmartWalletProxy: 0xf351Dd5EC89e5ac6c9125262853c74E714C1d56a
Multichain USDC: 0x04068DA6C83AFCFA0e13ba15A6696662335D5B75


SmartWalletProxy
Function: swap((address,uint256,uint256,address[],uint8,uint256,address,bytes))
0	params.swapContract	address	0x848c15AB2330285Bbe0740f11B97b2ac530FB881
0	params.srcAmount	uint256	400000
0	params.minDestAmount	uint256	927778291380739500
0	params.tradePath	address	0x04068DA6C83AFCFA0e13ba15A6696662335D5B75,0xAd84341756Bf337f5a0164515b1f6F993D194E1f,0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
0	params.feeMode	uint8	1
0	params.feeBps	uint256	0
0	params.platformWallet	address	0x168E4c3AC8d89B00958B6bE6400B066f0347DDc9
0	params.extraArgs	bytes	0x1b02da8cb0d097eb8d57a175b88c7d8b47997506


IERC20Ext internal constant ETH_TOKEN_ADDRESS = IERC20Ext(
    0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
);
IERC20Ext internal constant USDT_TOKEN_ADDRESS = IERC20Ext(
    0xdAC17F958D2ee523a2206206994597C13D831ec7
);
IERC20Ext internal constant DAI_TOKEN_ADDRESS = IERC20Ext(
    0x6B175474E89094C44Da98b954EedeAC495271d0F
);
IERC20Ext internal constant USDC_TOKEN_ADDRESS = IERC20Ext(
    0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
);
IERC20Ext internal constant WBTC_TOKEN_ADDRESS = IERC20Ext(
    0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
);
IERC20Ext internal constant KNC_TOKEN_ADDRESS = IERC20Ext(
    0xdd974D5C2e2928deA5F71b9825b8b646686BD200
);

https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller

Command to exe: 
pyinstaller main.py --onefile --ta rget-arch x86_64
cp dist/main.exe main.exe



https://ftmscan.com/tx/0x9aa1b52b8e7b343c22c36f5d2a2a59241e505208488bca51637f30c9d878b0af
https://ftmscan.com/tx/0xae45dcf082940dbac3cf1d8269ed47c5d84e715732d9b75ab4f2531aeb8907ed
contract decode bydata here
https://ftmscan.com/address/0x617dee16b86534a5d792a4d7a62fb491b544111e#code

1. Ban đầu nick số 1 có số tiền là A(100 FTM, 1050 usdc, 40 dai)
2. B1: Nick số 1 thực hiện giao dịch Approve(usdc)
3. B2: Nick số 1 thực hiện giao dịch Approve(dai)
4. B3: Nick số 1 thực hiện giao dịch Swap(1010 usdc -> 1010 dai)
5. B4: Nick số 1 thực hiện giao dịch Swap(1010 dai -> 1010 usdc)
6. B5: Nick số 1 thực hiện giao dịch Transfer(All usdc -> nick 2)
7. B6: Nick số 1 thực hiện giao dịch Transfer(All dai -> nick 2)
8. B7: Nick số 1 thực hiện giao dịch Transfer(All ftm -> nick 2)

Txs gốc Swap 1010 USDC -> DAI
https://ftmscan.com/tx/0x4a9bc9393faf4775ad86209eea0a4848ca966219ee442c6ad64a768592bd8a42
Txs gốc Swap 1010 DAI -> USDC
https://ftmscan.com/tx/0x34694ae8fe2f53415e3d494c07b3973626675afffda7e96dc4f7426cc8855e33

TXS Fake
2023-04-30 17:15:44,036 | INFO | Swap DAI->USDC success: https://ftmscan.com/tx/0xe1b180f2a22cd1336b54c4701b18ac69046962e07c00fbfae86ef56fe0203058
2023-04-30 17:15:51,901 | INFO | Swap USDC->DAI success: https://ftmscan.com/tx/0xec6453d699b0d8c3e0b5e7063eed3eb0a2194416c034f941ba20368f56ee1ed1