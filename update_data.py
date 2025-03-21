import yfinance as yf
import pandas as pd
from supabase import create_client
import os

# Ambil kredensial dari variabel lingkungan
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Daftar 5 saham blue-chip IHSG
saham_list = ["TLKM.JK", "BBRI.JK", "BMRI.JK", "ASII.JK", "UNTR.JK"]

def update_database():
    all_data = []
    for kode in saham_list:
        try:
            saham = yf.Ticker(kode)
            dividen = saham.dividends
            if not dividen.empty:
                df = pd.DataFrame({
                    "tanggal": dividen.index.strftime("%Y-%m-%d"),
                    "saham": kode,
                    "dividen": dividen.values
                })
                all_data.append(df)
        except Exception as e:
            print(f"Gagal mengambil data untuk {kode}: {e}")

    if all_data:
        df_combined = pd.concat(all_data, ignore_index=True)
        data = df_combined.to_dict(orient="records")
        supabase.table("dividen").upsert(data).execute()
        print(f"Berhasil menyimpan {len(data)} baris ke database!")
    else:
        print("Tidak ada data baru untuk disimpan.")

if __name__ == "__main__":
    update_database()