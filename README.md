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
pyinstaller main.py --onefile
cp dist/main.exe main.exe