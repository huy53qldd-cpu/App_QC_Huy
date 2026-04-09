import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import toml # Thêm thư viện này để đọc định dạng TOML

def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Đọc file key.json theo kiểu TOML
    with open("key.json", "r") as f:
        config = toml.load(f)
    
    creds_dict = dict(config["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    client = gspread.authorize(creds)
    sheet = client.open("data").sheet1
    return pd.DataFrame(sheet.get_all_records())

st.title("🔍 Tra cứu Linh kiện QC")

try:
    df = load_data()
    list_ma_lk = df['Mã LK'].astype(str).unique().tolist()
    ma_chon = st.selectbox("Chọn Mã linh kiện:", options=[""] + list_ma_lk)
    
    if ma_chon:
        ket_qua = df[df['Mã LK'].astype(str) == ma_chon]
        st.info(f"**Tên LK:** {ket_qua.iloc[0]['Tên LK']}")
        st.metric("Giá bán", f"{ket_qua.iloc[0]['Giá bán']:,} VNĐ")
except Exception as e:
    st.error(f"Lỗi: {e}")
