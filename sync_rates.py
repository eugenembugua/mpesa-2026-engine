import json
import requests

def sync_broker_data(json_path='hakikisha.json'):
    #Fetch live rates from "Broker" 
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=kes"
    
    try:
        response = requests.get(url)
        rates = response.json()
        
        btc_kes = rates['bitcoin']['kes']
        eth_kes = rates['ethereum']['kes']

        #Load your current DB
        with open(json_path, 'r') as f:
            db = json.load(f)

        #Update CRYPTO_RATES
        db["CRYPTO_RATES"] = {
            "BTC": btc_kes,
            "ETH": eth_kes
        }

        #Update WALLET Names to Broker Names
        if "0xABC123" in db["CRYPTO_WALLETS"]:
            db["CRYPTO_WALLETS"]["0xABC123"]["name"] = "YellowCard Broker (BTC)"
        
        if "0scAW567" in db["CRYPTO_WALLETS"]:
            db["CRYPTO_WALLETS"]["0scAW567"]["name"] = "YellowCard Broker (ETH)"

        #Save back to hakikisha.json
        with open(json_path, 'w') as f:
            json.dump(db, f, indent=4)
        
        print(f"Successfully synced with Broker. BTC: {btc_kes:,} KES | ETH: {eth_kes:,} KES")

    except Exception as e:
        print(f"Connection to Broker failed: {e}")

if __name__ == "__main__":
    sync_broker_data()