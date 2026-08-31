import yfinance as yf, time, os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

WATCH = ["BBCA.JK","BBRI.JK","BBNI.JK","TLKM.JK","ADRO.JK","INET.JK","BIPI.JK"]

def update_prices():
    print("--- Fetching Real BEI (Mode Weekend OK) ---")
    for code in WATCH:
        try:
            ticker = yf.Ticker(code)
            hist = ticker.history(period="5d", interval="1d")
            if not hist.empty:
                price = float(hist['Close'].iloc[-1])
                vol = int(hist['Volume'].iloc[-1])
                emiten = code.replace(".JK","")
                supabase.table("live_prices").upsert({
                    "emiten": emiten, 
                    "price": price, 
                    "volume": vol
                }).execute()
                print(f"OK {emiten}: {price} Vol:{vol}")
            time.sleep(1)
        except Exception as e:
            print(f"Error {code}: {e}")
    print("Done, sleep 60 detik")

while True:
    update_prices()
    time.sleep(60)
