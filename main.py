import gspread
import requests
import json
import os
import sys
import pandas as pd



# ERC-20 tokens come in 18 decimals



# Not yet in use
data = {
    'Chain Name': [
        'Ethereum Mainnet', 'Sepolia Testnet', 'Holesky Testnet', 'Abstract Mainnet', 'Abstract Sepolia Testnet',
        'ApeChain Curtis Testnet', 'ApeChain Mainnet', 'Arbitrum Nova Mainnet', 'Arbitrum One Mainnet', 'Arbitrum Sepolia Testnet',
        'Avalanche C-Chain', 'Avalanche Fuji Testnet', 'Base Mainnet', 'Base Sepolia Testnet', 'Berachain Mainnet',
        'BitTorrent Chain Mainnet', 'BitTorrent Chain Testnet', 'Blast Mainnet', 'Blast Sepolia Testnet', 'BNB Smart Chain Mainnet',
        'BNB Smart Chain Testnet', 'Celo Alfajores Testnet', 'Celo Mainnet', 'Cronos Mainnet', 'Fraxtal Mainnet',
        'Fraxtal Testnet', 'Gnosis', 'Linea Mainnet', 'Linea Sepolia Testnet', 'Mantle Mainnet', 'Mantle Sepolia Testnet',
        'Moonbase Alpha Testnet', 'Moonbeam Mainnet', 'Moonriver Mainnet', 'OP Mainnet', 'OP Sepolia Testnet', 'Polygon Amoy Testnet',
        'Polygon Mainnet', 'Polygon zkEVM Cardona Testnet', 'Polygon zkEVM Mainnet', 'Scroll Mainnet', 'Scroll Sepolia Testnet',
        'Sonic Blaze Testnet', 'Sonic Mainnet', 'Sophon Mainnet', 'Sophon Sepolia Testnet', 'Taiko Hekla L2 Testnet',
        'Taiko Mainnet', 'Unichain Mainnet', 'Unichain Sepolia Testnet', 'WEMIX3.0 Mainnet', 'WEMIX3.0 Testnet',
        'World Mainnet', 'World Sepolia Testnet', 'Xai Mainnet', 'Xai Sepolia Testnet', 'XDC Apothem Testnet', 'XDC Mainnet',
        'zkSync Mainnet', 'zkSync Sepolia Testnet'
    ],
    'Chain ID': [
        1, 11155111, 17000, 2741, 11124, 33111, 33139, 42170, 42161, 421614, 43114, 43113, 8453, 84532, 80094,
        199, 1028, 81457, 168587773, 56, 97, 44787, 42220, 25, 252, 2522, 100, 59144, 59141, 5000, 5003, 1287, 1284,
        1285, 10, 11155420, 80002, 137, 2442, 1101, 534352, 534351, 57054, 146, 50104, 531050104, 167009, 167000, 130,
        1301, 1111, 1112, 480, 4801, 660279, 37714555429, 51, 50, 324, 300
    ],
    'Ticker': [
        'ETH', 'ETH-SEP', 'ETH-HOLESKY', 'ABS', 'ABS-SEP', 'APE-CURTIS', 'APE', 'ARB-NOVA', 'ARB', 'ARB-SEP', 'AVAX', 'AVAX-FUJI',
        'BASE', 'BASE-SEP', 'BERA', 'BTT', 'BTT-TEST', 'BLAST', 'BLAST-SEP', 'BNB', 'BNB-TEST', 'CELO-AF', 'CELO', 'CRO', 'FRX',
        'FRX-TEST', 'GNO', 'LINEA', 'LINEA-SEP', 'MNT', 'MNT-SEP', 'MOONBASE-ALPHA', 'MOONBEAM', 'MOONRIVER', 'OP', 'OP-SEP',
        'POLY-AMOY', 'POLY', 'POLY-ZK-TEST', 'POLY-ZK', 'SCROLL', 'SCROLL-SEP', 'SONIC-BLAZE', 'SONIC', 'SOPHON', 'SOPHON-SEP',
        'TAIKO-HEKLA', 'TAIKO', 'UNI', 'UNI-SEP', 'WEMIX', 'WEMIX-TEST', 'WORLD', 'WORLD-SEP', 'XAI', 'XAI-SEP', 'XDC-APOTHEM',
        'XDC', 'ZKSYNC', 'ZKSYNC-SEP'
    ]
}
etherscan_lookup = pd.DataFrame(data)



def authenticate_google_sheets(credentials, sheet_name):
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open(sheet_name)
    return sh.sheet1

# Fetch wallet balance from a blockchain explorer API
def get_wallet_balance(wallet_address, crypto):
    print(crypto)
    if crypto == "AAVE":
      url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x7Fc66500c84b76Ba3b6b5644d1d5caa4b8b3a1b8&address={wallet_address}&tag=latest"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  # AAVE has 18 decimals
      staked_balance = 0  # Not implemented
    elif crypto == "ADA":
      url = f"https://cardano-mainnet.blockfrost.io/api/v0/addresses/{wallet_address}"
      headers = {"project_id": "YourBlockfrostAPIKey"}
      response = requests.get(url, headers=headers)
      data = response.json()
      balance = float(data['balance']) / 10 ** 6 
      staked_balance = 0  # Not implemented
    elif crypto == "ALPH":
      url = f"https://backend.mainnet.alephium.org/addresses/{wallet_address}/balance"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance']) / 10**18
      staked_balance = 0 # Not implemented
    elif crypto == "ARB":
      url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x912ce59144191c1204e64559e4d3e1e4e2f8d25c&address={wallet_address}&tag=latest"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18 
      staked_balance = 0  # N/A
    elif crypto == "AVAX":
      url = f"https://api.snowtrace.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey=YourApiKeyToken"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  
      staked_balance = 0 # Not implemented
    elif crypto == "BCH":
      url = f"https://api.blockchair.com/bitcoin-cash/dashboards/address/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['data'][wallet_address]['address']['balance']) / 10 ** 8
      staked_balance = 0 # Not implemented
    elif crypto == "BNB":
      url = f"https://api.bscscan.com/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey=YourApiKeyToken"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  
      staked_balance = 0 # Not implemented
    elif crypto == "BONK":
      url = f"https://api.solscan.io/account/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['data']['lamports']) / 10 ** 9 
      staked_balance = 0 # Not implemented
    elif crypto == "BTC":
      url = f"https://blockchain.info/rawaddr/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['final_balance']) / 10 ** 8
      staked_balance = 0 # N/A
    elif crypto == "CAKE":
      url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address={wallet_address}&tag=latest"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  # CAKE has 18 decimals
      staked_balance = 0  # Not implemented
    elif crypto == "COMP":
      url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xc00e94cb662c3520282e6f5717214004a7f26888&address={wallet_address}&tag=latest"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  
      staked_balance = 0  # N/A
    elif crypto == "DASH":
      url = f"https://api.blockchair.com/dash/dashboards/address/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['data'][wallet_address]['address']['balance']) / 10 ** 8
      staked_balance = 0 # Not implemented
    elif crypto == "DCR":
      url = f"https://explorer.dcrdata.org/api/address/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance']['total'])
      staked_balance = float(data['balance']['stake'])
    elif crypto == "DOGE":
      url = f"https://dogechain.info/api/v1/address/balance/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance'])
      staked_balance = 0 # N/A
    elif crypto == "ETC":
      url = f"https://etc.blockscout.com/api/v2/addresses/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['coin_balance']) / 10 ** 18
      staked_balance = 0 # Not implemented
    elif crypto == "ETH":
      url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey=YourApiKeyToken"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  # ETH is in wei
      staked_balance = 0 # Not implemented
    elif crypto == "FLUX":
      url = f"https://explorer.runonflux.io/api/addr/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance'])
      staked_balance = 0 # Not implemented
    elif crypto == "KAS":
      wallet_address=wallet_address.replace(":", "%3A")
      url = f"https://api.kaspa.org/addresses/{wallet_address}/balance"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance']) / 10 ** 8
      staked_balance = 0 # N/A
    elif crypto == "LEO":
      url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x2af5d2ad767e5dcb8a1f1f7e7c7adf8a9f3d3b97&address={wallet_address}&tag=latest&apikey=YourApiKeyToken"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  
      staked_balance = 0 # N/A
    elif crypto == "LINK":
      url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x514910771af9ca656af840dff83e8264ecf986ca&address={wallet_address}&tag=latest&apikey=YourApiKeyToken"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18
      staked_balance = 0 # N/A
    elif crypto == "LTC":
      url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{wallet_address}/balance"
      response = requests.get(url)
      data = response.json()
      balance = float(data['final_balance']) / 10 ** 8
      staked_balance = 0 # N/A
    elif crypto == "OCTA":
      url = f"https://explorer.octa.space/api?module=account&action=balance&address={wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18
      staked_balance = 0 # Not implemented
    elif crypto == "RVN":
      url = f"https://rvn.cryptoscope.io/api/addr/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance'])
      staked_balance = 0 # N/A
    elif crypto == "SHIB":
      url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE&address={wallet_address}&tag=latest"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  
      staked_balance = 0  # Not implemented
    elif crypto == "SOL":
      url = f"https://api.solscan.io/account/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['data']['lamports']) / 10 ** 9 
      staked_balance = 0 # Not implemented
    elif crypto == "TON":
      url = f"https://tonapi.io/v1/account/{wallet_address}/balance"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance']) / 10 ** 9
      staked_balance = 0  # Not implemented
    elif crypto == "TRUMP":
      url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x2A4e3a88c14F7f1bE199A4aCd2a7e8F2B0526D49&address={wallet_address}&tag=latest"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18 
      staked_balance = 0  # Not implemented
    elif crypto == "TRX":
      url = f"https://api.tronscan.org/api/account?address={wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['data']['balance']) / 10 ** 6  
      staked_balance = 0  # Not implemented
    elif crypto == "WIF":
      url = f"https://api.solscan.io/account/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['data']['lamports']) / 10 ** 9  
      staked_balance = 0 # Not implemented
    elif crypto == "XCH":
      url = f"https://api.spacescan.io/address/balance/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['data']['balance']['xch'])
      staked_balance = 0 # Not implemented
    elif crypto == "XLM":
      url = f"https://horizon.stellar.org/accounts/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balances'][0]['balance'])  
      staked_balance = 0  # N/A
    elif crypto == "XRP":
      url = f"https://data.ripple.com/v2/accounts/{wallet_address}/balances"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balances'][0]['value'])  # XRP balance
      staked_balance = 0 # N/A
    elif crypto == "XTZ":
      url = f"https://api.tzkt.io/v1/accounts/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance']) / 10 ** 6 
      staked_balance = float(data['stakingBalance']) / 10 ** 6
    elif crypto == "UNI":
      url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x5C69bEe701ef814a2B6a3EDD4B4aBC2c79b3bF8e&address={wallet_address}&tag=latest"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18  
      staked_balance = 0  # N/A
    elif crypto == "ZIL":
      url = "https://api.zilliqa.com/"
      headers = {"Content-Type": "application/json"}
      data = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": "GetBalance",
        "params": [wallet_address]
      }
      response = requests.post(url, headers=headers, json=data)
      data = response.json()
      balance = float(data['result']['balance']) / 10 ** 12

      staking_contract = os.getenv("ZIL_STAKING_CONTRACT_ADDRESS")
      staked_data = {
        "id": "2",
        "jsonrpc": "2.0",
        "method": "GetSmartContractSubState",
        "params": [
            staking_contract,  # Smart contract address
            "stakers",         # Field to query
            [wallet_address]   # Your wallet address
        ]
      }
      staked_response = requests.post(url, headers=headers, json=staked_data)
      staked_result = staked_response.json()

      if "result" in staked_result and "stakers" in staked_result["result"]:
        staked_balance = float(staked_result["result"]["stakers"].get(wallet_address, 0)) / 10 ** 12
      else:
        staked_balance = 0.0
    elif etherscan_lookup['Ticker'].str.contains(crypto).any():
       # TODO
       balance = 0
       staked_balance = 0
    else:
      balance = 0
      staked_balance = 0
    return balance, staked_balance

# Fetch current crypto price in USD
def get_crypto_price(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return float(data[crypto]['usd'])  # Adjust according to the API response

# Update Google Sheets
def update_google_sheet(sheet, start_row=2):
    wallet_addresses = sheet.col_values(1)[start_row - 1:]
    cryptos = sheet.col_values(2)[start_row - 1:]
    for i, (wallet, crypto) in enumerate(zip(wallet_addresses, cryptos), start=start_row):
        if wallet and crypto:
            try:
                balance, staked_balance = get_wallet_balance(wallet, crypto)
                sheet.update_cell(i, 3, balance)
                sheet.update_cell(i, 4, staked_balance)
            except Exception as e:
                print(f"Error updating row {i}: {e}")


if __name__ == "__main__":
    credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    SHEET_NAME = os.getenv("SHEET_NAME")
    if not credentials:
        print("Environment variables 'secret.json' is not set.", file=sys.stderr)
        sys.exit(1)
    if not SHEET_NAME:
        print("Environment variables 'SHEET_NAME' is not set.", file=sys.stderr)
        sys.exit(1)
    credentials = json.loads(credentials)
    sheet = authenticate_google_sheets(credentials, SHEET_NAME)
    update_google_sheet(sheet)