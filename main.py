import gspread
import requests
import json
import os
import sys

def authenticate_google_sheets(credentials, sheet_name):
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open(sheet_name)# Access the first sheet in the workbook

# Fetch wallet balance from a blockchain explorer API
def get_wallet_balance(wallet_address, crypto):
    print(crypto)
    if crypto == "ALPH":
      url = f"https://backend.mainnet.alephium.org/addresses/{wallet_address}/balance"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance']) / 10**18
    elif crypto == "BTC":
      url = f"https://blockchain.info/rawaddr/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['final_balance']) / 10 ** 8
    elif crypto == "ETC":
      url = f"https://etc.blockscout.com/api/v2/addresses/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['coin_balance']) / 10 ** 18
    elif crypto == "KAS":
      wallet_address=wallet_address.replace(":", "%3A")
      url = f"https://api.kaspa.org/addresses/{wallet_address}/balance"
      response = requests.get(url)
      data = response.json()
      balance = float(data['balance']) / 10 ** 8
    elif crypto == "OCTA":
      url = f"https://explorer.octa.space/api?module=account&action=balance&address={wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['result']) / 10 ** 18
    elif crypto == "XCH":
      url = f"https://api.spacescan.io/address/balance/{wallet_address}"
      response = requests.get(url)
      data = response.json()
      balance = float(data['data']['balance']['xch'])

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
    else:
      url = f"https://api.blockchainexplorer.com/balance/{crypto}/{wallet_address}"
      response = requests.get(url)
      data = response.json()
    return balance  # Adjust according to the API response

# Fetch current crypto price in USD
def get_crypto_price(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return float(data[crypto]['usd'])  # Adjust according to the API response

# Update Google Sheets
def update_google_sheet(sheet, start_row=2):
    # Read wallet addresses and cryptocurrencies from the sheet
    wallet_addresses = sheet.col_values(1)[start_row - 1:]
    cryptos = sheet.col_values(2)[start_row - 1:]
    for i, (wallet, crypto) in enumerate(zip(wallet_addresses, cryptos), start=start_row):
        if wallet and crypto:
            try:
                balance = get_wallet_balance(wallet, crypto)
                sheet.update_cell(i, 3, balance)  # Column C: Balance
            except Exception as e:
                print(f"Error updating row {i}: {e}")


if __name__ == "__main__":
    credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    SHEET_NAME = os.getenv("SHEET_NAME")
    print(credentials)
    if not credentials:
        print("Environment variables 'secret.json' is not set.", file=sys.stderr)
        sys.exit(1)
    if not SHEET_NAME:
        print("Environment variables 'SHEET_NAME' is not set.", file=sys.stderr)
        sys.exit(1)
    credentials = json.loads(credentials)
    sheet = authenticate_google_sheets(credentials, SHEET_NAME)
    update_google_sheet(sheet)