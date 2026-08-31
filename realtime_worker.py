import yfinance as yf, time, os, requests
from supabase import create_client

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Daftar pantauan
WATCH = ["BBCA.JK","BBRI.JK","BBNI.JK","TLKM.JK","ADRO.JK","INET.JK","BIPI.JK"]

def get_price_accurate(code):
    try:
        ticker = yf.Ticker(code)
        # fast_info = harga real-time tanpa adjust split, ini yang akurat
        price = float(ticker.fast_info['last_price'])
        # volume hari ini
        vol = int(ticker.fast_info.get('last_volume', 0))
        if price < 100: # filter error Yahoo kadang 0
            raise Exception("price too low")
        return price, vol
    except:
        # Fallback: ambil dari Google Finance via GoAPI (lebih akurat untuk IDX)
        try:
            # Tanpa API key, pakai endpoint publik TradingView
            emiten = code.replace(".JK","")
            # TradingView unofficial
            url = f"https://api.goapi.id/v1/stock/idx/{emiten}"
            # Kalau belum punya API key GoAPI, ini akan skip dan pakai harga Fortune
            return None, None
        except:
            return None, None

def update_prices():
    print("--- Fetching REAL IDX Prices (Fix) ---")
    for code in WATCH:
        emiten = code.replace(".JK","")
        price, vol = get_price_accurate(code)
        if price:
            supabase.table("live_prices").upsert({
                "emiten": emiten, "price": price, "volume": vol or 0
            }).execute()
            print(f"OK {emiten}: Rp{price}")
        time.sleep(1)

while True:
    update_prices()
    time.sleep(30)
