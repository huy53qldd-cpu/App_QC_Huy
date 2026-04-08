import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 1. Hàm kết nối Google Sheets (Cloud Database)
def load_data():
    # Khai báo quyền truy cập
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # File chìa khóa key.json phải nằm cùng thư mục với file app.py này
    creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
    client = gspread.authorize(creds)
    
    # Mở file Google Sheets tên là "data" (Huy kiểm tra đúng tên file trên Drive nhé)
    sheet = client.open("data").sheet1
    
    # Đọc toàn bộ dữ liệu vào bảng Pandas
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# 2. Cấu hình giao diện App
st.set_page_config(page_title="App QC Huy", layout="centered")
st.title("🔍 Tra cứu Linh kiện QC")

try:
    # Tải dữ liệu từ Sheet
    df = load_data()
    
    # Lấy danh sách tất cả Mã LK để làm danh sách gợi ý
    list_ma_lk = df['Mã LK'].astype(str).unique().tolist()

    # Tạo ô nhập liệu có tính năng Gợi ý (Suggest)
    # Streamlit dùng st.selectbox để người dùng vừa gõ vừa chọn mã rất nhanh
    ma_chon = st.selectbox(
        "Nhập hoặc chọn Mã linh kiện để tra cứu:",
        options=[""] + list_ma_lk,
        format_func=lambda x: "--- Đang chờ nhập mã ---" if x == "" else x
    )

    # Khi người dùng chọn một mã (khác khoảng trống)
    if ma_chon != "":
        # Lọc thông tin linh kiện tương ứng
        ket_qua = df[df['Mã LK'].astype(str) == ma_chon]

        if not ket_qua.empty:
            st.divider() # Dòng kẻ ngăn cách
            
            # Hiển thị thông tin Tên LK và Giá bán
            st.subheader(f"Kết quả cho mã: {ma_chon}")
            
            # Chia làm 2 cột cho đẹp trên máy tính, tự xếp chồng trên điện thoại
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"**Tên Linh Kiện:**\n\n{ket_qua.iloc[0]['Tên LK']}")
            
            with col2:
                gia = ket_qua.iloc[0]['Giá bán']
                # Hiển thị giá dạng số to, rõ ràng
                st.metric(label="Giá bán", value=f"{gia:,} VNĐ")
        else:
            st.error("Không tìm thấy dữ liệu cho mã này!")

except Exception as e:
    st.error("Lỗi kết nối!")
    st.write(f"Chi tiết lỗi: {e}")
    st.info("Huy kiểm tra lại: 1. File 'key.json' đã để cạnh file 'app.py' chưa? 2. Đã Share quyền Editor cho email nm010198...@... chưa?")