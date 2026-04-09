import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Hàm lấy dữ liệu
def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Lệnh này sẽ đọc đúng cái file key.json Huy vừa sửa
    creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
    client = gspread.authorize(creds)
    # Nhớ tên file Google Sheets của Huy phải là "data" nhé
    sheet = client.open("data").sheet1
    return pd.DataFrame(sheet.get_all_records())
    
    # Mở file Google Sheets (Huy nhớ đặt tên file Excel trên Drive đúng là "data" nhé)
    sheet = client.open("data").sheet1
    return pd.DataFrame(sheet.get_all_records())

# Cấu hình giao diện
st.set_page_config(page_title="App QC Hải Phòng", page_icon="🔍")
st.title("🔍 Tra cứu Linh kiện QC")

try:
    df = load_data()
    
    # Tạo danh sách mã linh kiện để chọn
    list_ma_lk = df['Mã LK'].astype(str).unique().tolist()
    
    ma_chon = st.selectbox(
        "Nhập hoặc chọn Mã linh kiện:",
        options=[""] + list_ma_lk,
        format_func=lambda x: "--- Đang chờ nhập mã ---" if x == "" else x
    )

    if ma_chon != "":
        # Lọc dữ liệu theo mã đã chọn
        ket_qua = df[df['Mã LK'].astype(str) == ma_chon]
        
        if not ket_qua.empty:
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Tên Linh Kiện:**\n\n{ket_qua.iloc[0]['Tên LK']}")
            with col2:
                gia = ket_qua.iloc[0]['Giá bán']
                st.metric(label="Giá bán", value=f"{gia:,} VNĐ")
        else:
            st.warning("Không tìm thấy thông tin cho mã này!")

except Exception as e:
    st.error("Lỗi kết nối dữ liệu!")
    st.write(f"Chi tiết lỗi: {e}")
