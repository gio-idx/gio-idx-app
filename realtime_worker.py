import yfinance as yf, time, os
from supabase import create_client

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
WATCH = ["BBCA.JK","BBRI.JK","BBNI.JK","TLKM.JK","ADRO.JK","INET.JK","BIPI.JK"]

while True:
    try:
        data = yf.download(WATCH, period="1d", interval="1m", progress=False)
        for code in WATCH:
            emiten = code.replace(".JK","")
            price = float(data[code]['Close'].dropna().iloc[-1])
            vol = int(data[code]['Volume'].dropna().iloc[-1])
            supabase.table("live_prices").upsert({"emiten": emiten, "price": price, "volume": vol}).execute()
            print(f"Update {emiten}: {price}")
    except Exception as e:
        print(e)
    time.sleep(15) # update tiap 15 detik
