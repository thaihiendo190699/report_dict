import streamlit as st
from PIL import Image

 # --- Cache image loading to speed up ---
@st.cache_data
def load_image(path,size=(300,300)):
    # return Image.open(path)
    img = Image.open(path)
    img.thumbnail(size)
    return img

def display_info(cols,col_index,photo,name,email,role=''):
    with cols[col_index]:
        img = load_image(photo)
        st.image(img, use_column_width=True)
        if role:
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <strong>{name}</strong><br>
                    {role}<br>
                    <a href='mailto:{email}'>{email}</a>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
            f"""
            <div style='text-align: center;'>
                <strong>{name}</strong><br>
                <a href='mailto:{email}'>{email}</a>
            </div>
            """,
            unsafe_allow_html=True
            )

def contact_info():
    st.title("🪪 Contact Info")

    # --- Team Members Data ---
    team = [
        {
            "name": r"Nguyễn Hoàng Đăng Quân",
            "photo": "photo/Quan.jpg",
            "role": "Strategic Planning Lead",
            "email": "Quan.Nguyen@sony.com"
        },
        {
            "name": r"Lê Việt Thái",
            "photo":"photo/Thai.jpg",
            "role": "",
            "email": "Thai.Le@sony.com"
        },
        {
            "name": r"Trần Thị Cẩm Tiên",
            "photo":"photo/Tien.jpg",
            "role": "",
            "email": "Tien.TranCam@sony.com"
        },
        {
            "name": r"Đỗ Thị Thái Hiền",
            "photo":"photo/Hien.jpg",
            "role": "",
            "email": "Hien.Do@sony.com"
        },
        {
            "name": r"Nguyễn Ngọc Thảo Như",
            "photo":"photo/Nhu.png",
            "role": "",
            "email": "Nhu.NguyenNT@sony.com"
        }
    ]

    # --- Display Members in Columns ---
    with st.spinner("Loading team members..."):
        for index, member in enumerate(team,start=0):
            cols = st.columns(3)  # 3 columns
            display_info(cols,1,member["photo"],member['name'],member['email'],member['role'])