import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 1. Hàm kết nối bằng file key.json trực tiếp
def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # App sẽ tự đọc file key.json nằm cùng thư mục trên GitHub
    creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
    client = gspread.authorize(creds)
    
    # Mở file Google Sheets tên là "data"
    sheet = client.open("data").sheet1
    return pd.DataFrame(sheet.get_all_records())

# Giao diện App
st.set_page_config(page_title="App QC Huy", layout="centered")
st.title("🔍 Tra cứu Linh kiện QC")

try:
    df = load_data()
    # Lấy danh sách mã LK
    list_ma_lk = df['Mã LK'].astype(str).unique().tolist()

    ma_chon = st.selectbox(
        "Nhập hoặc chọn Mã linh kiện:",
        options=[""] + list_ma_lk,
        format_func=lambda x: "--- Đang chờ nhập mã ---" if x == "" else x
    )

    if ma_chon != "":
        ket_qua = df[df['Mã LK'].astype(str) == ma_chon]
        if not ket_qua.empty:
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Tên LK:**\n\n{ket_qua.iloc[0]['Tên LK']}")
            with col2:
                gia = ket_qua.iloc[0]['Giá bán']
                st.metric(label="Giá bán", value=f"{gia:,} VNĐ")
except Exception as e:
    st.error("Lỗi kết nối!")
    st.write(f"Chi tiết: {e}")
