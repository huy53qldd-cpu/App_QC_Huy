import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 1. Hàm kết nối và lấy dữ liệu từ Google Sheets
def load_data():
    # Khai báo quyền truy cập
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Đọc file chìa khóa key.json nằm cùng thư mục trên GitHub
    # Đảm bảo Huy đã upload file key.json chuẩn (định dạng dấu ngoặc nhọn {}) lên GitHub
    creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
    client = gspread.authorize(creds)
    
    # Mở file Google Sheets tên là "data"
    # Huy nhớ đặt tên file Excel trên Drive là "data" (viết thường, không đuôi .xlsx)
    sheet = client.open("data").sheet1
    
    # Chuyển dữ liệu thành bảng (DataFrame)
    return pd.DataFrame(sheet.get_all_records())

# 2. Cấu hình giao diện App
st.set_page_config(page_title="App QC Hải Phòng", page_icon="🔍", layout="centered")

# Tiêu đề chính
st.title("🔍 Tra cứu Linh kiện QC")
st.markdown("---")

try:
    # Gọi hàm lấy dữ liệu
    df = load_data()
    
    # Chuyển cột 'Mã LK' thành dạng chữ để tránh lỗi định dạng số
    df['Mã LK'] = df['Mã LK'].astype(str)

    # Tạo danh sách mã linh kiện để người dùng chọn
    list_ma_lk = df['Mã LK'].unique().tolist()

    # Ô chọn mã linh kiện
    ma_chon = st.selectbox(
        "Nhập hoặc chọn Mã linh kiện:",
        options=[""] + list_ma_lk,
        format_func=lambda x: "--- Mời bạn chọn mã ---" if x == "" else x
    )

    # Nếu đã chọn một mã cụ thể
    if ma_chon != "":
        # Lọc dữ liệu trong bảng
        ket_qua = df[df['Mã LK'] == ma_chon]
        
        if not ket_qua.empty:
            st.success(f"Đã tìm thấy thông tin cho mã: **{ma_chon}**")
            
            # Hiển thị thông tin thành 2 cột cho đẹp
            col1, col2 = st.columns(2)
            
            with col1:
                ten_lk = ket_qua.iloc[0]['Tên LK']
                st.info(f"**Tên Linh Kiện:**\n\n{ten_lk}")
                
            with col2:
                # Lấy giá bán và định dạng có dấu phẩy ngăn cách nghìn
                gia = ket_qua.iloc[0]['Giá bán']
                try:
                    gia_so = float(gia)
                    st.metric(label="Giá bán", value=f"{gia_so:,.0f} VNĐ")
                except:
