import streamlit as st
from PIL import Image

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

    # --- Cache image loading to speed up ---
    @st.cache_data
    def load_image(path,size=(300,300)):
        # return Image.open(path)
        img = Image.open(path)
        img.thumbnail(size)
        return img
        # return load_image_fixed(path, size=(300, 300))

    # --- Display Members in Columns ---
    with st.spinner("Loading team members..."):
        cols = st.columns(5)  # 3 columns
        for i, member in enumerate(team[:3]):
            with cols[i+1]:
                img = load_image(member["photo"])
                st.image(img, use_column_width=True)
                if member['role']:
                    st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <strong>{member['name']}</strong><br>
                            {member['role']}<br>
                            <a href='mailto:{member['email']}'>{member['email']}</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                     st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <strong>{member['name']}</strong><br>
                            <a href='mailto:{member['email']}'>{member['email']}</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            
        cols2 = st.columns(4)
        for i, member in enumerate(team[3:5]):
            with cols2[i+1]:
                img = load_image(member["photo"])
                st.image(img, use_column_width=True)
                st.markdown(
                    f"""
                    <div style='text-align: center;'>
                        <strong>{member['name']}</strong><br>
                        {member['role']}<br>
                        <a href='mailto:{member['email']}'>{member['email']}</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
