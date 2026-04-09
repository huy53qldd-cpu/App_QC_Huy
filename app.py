import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Lấy chìa khóa từ Secrets của Streamlit Cloud
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # Mở file Google Sheets tên là "data"
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