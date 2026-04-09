import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Dùng thư viện json để đọc file chắc chắn 100% không bị lỗi định dạng
    with open("key.json", "r", encoding="utf-8") as f:
        creds_dict = json.load(f)
        
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("data").sheet1
    return pd.DataFrame(sheet.get_all_records())

st.set_page_config(page_title="App QC Hải Phòng", page_icon="🔍", layout="centered")

st.title("🔍 Tra cứu Linh kiện QC")
st.markdown("---")

try:
    df = load_data()
    
    df['Mã LK'] = df['Mã LK'].astype(str)
    list_ma_lk = df['Mã LK'].unique().tolist()

    ma_chon = st.selectbox(
        "Nhập hoặc chọn Mã linh kiện:",
        options=[""] + list_ma_lk,
        format_func=lambda x: "--- Mời bạn chọn mã ---" if x == "" else x
    )

    if ma_chon != "":
        ket_qua = df[df['Mã LK'] == ma_chon]
        
        if not ket_qua.empty:
            st.success(f"Đã tìm thấy thông tin cho mã: **{ma_chon}**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                ten_lk = ket_qua.iloc[0]['Tên LK']
                st.info(f"**Tên Linh Kiện:**\n\n{ten_lk}")
                
            with col2:
                gia = ket_qua.iloc[0]['Giá bán']
                try:
                    gia_so = float(gia)
                    st.metric(label="Giá bán", value=f"{gia_so:,.0f} VNĐ")
                except:
                    st.metric(label="Giá bán", value=f"{gia} VNĐ")
        else:
            st.warning("Không tìm thấy dữ liệu cho mã này!")

except Exception as e:
    st.error("⚠️ Lỗi kết nối dữ liệu!")
    st.write("Chi tiết lỗi kỹ thuật:")
    st.code(e)
