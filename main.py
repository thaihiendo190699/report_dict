from report_dictionary_page import report_dictionary
from contact_info_page import contact_info
import time

import webbrowser
import streamlit as st


# st.logo('snp_logo.png',size="large")
# Initialize the selected page
st.set_page_config(page_title="Strategic Planning",
                    layout="wide",
                    page_icon="🔥")

if "page" not in st.session_state:
    st.session_state.page = "report_dictionary"

def sidebar_button(name,page_dict):
    # Handle internal page navigation
    if page_dict['reference_type']=="page":
        if st.sidebar.button(page_dict['label'], use_container_width=True):
            st.session_state.page =name

    elif page_dict['reference_type']=="link":
        st.sidebar.markdown(
            f"""
            <style>
            .sidebar-link {{
                display: inline-flex;
                -webkit-box-align: center;
                align-items: center;
                -webkit-box-pack: center;
                justify-content: center;
                font-weight: 400;
                padding: 0.25rem 0.75rem;
                border-radius: 0.5rem;
                min-height: 2.5rem;
                margin: 0px;
                line-height: 1.6;
                text-transform: none;
                font-size: inherit;
                font-family: inherit;
                color: inherit;
                width: 100%;
                user-select: none;
                background-color: rgb(249, 249, 251);
                border: 1px solid rgba(49, 51, 63, 0.2);
                text-decoration: none !important;
            }}
            .sidebar-link:hover {{
                background-color: #F0F0F0;
                border-color: 1px solid #1E90FF;
            }}
            </style>

            <a href="{page_dict['link']}" target="_blank" class="sidebar-link">{page_dict['label']}</a>

            """,
            unsafe_allow_html=True
        )

# Sidebar Navigation
st.sidebar.title("Strategic Planning")
st.sidebar.header("Navigation")
pages = {"report_dictionary":{"label":"🔍 Report Dictionary",
                            "reference_type":"page",
                            "page":report_dictionary},
        "CI_validation":{"label":"🗂️ CI validation",
                        "reference_type":"link",
                         "link":r"http://43.94.1.64:8683/"},
        "Contact_us":{"label":"🪪 Contact info",
                    "reference_type":"page",
                    "page":contact_info}     
        }

for p in pages:
    sidebar_button(name=p,page_dict=pages[p])

with st.spinner(f"Loading {pages[st.session_state.page]["label"]}..."):
    page=pages[st.session_state.page]["page"]
    page()

# # --- Detect query param for internal navigation ---
# query_params = st.experimental_get_query_params()
# if "page" in query_params:
#     st.session_state.page = query_params["page"][0]
#     print(st.session_state.page)

# # Display selected page
# if st.session_state.page == "report_dictionary":
#     # st.title(st.session_state.page)
#     page=pages[st.session_state.page]["page"]
#     page()
#     # st.write("Welcome to Home!")

# # # elif st.session_state.page == "🔍 CI validation":
# # #     pass
# #     # webbrowser.open_new_tab("http://43.94.1.64:8683/")
# #     # st.title(st.session_state.page)
# #     # st.title("📊 Analytics Page")
# #     # st.write("Analytics data here.")
    
# # elif st.session_state.page == "Contact_us":
# #     page=pages[st.session_state.page]["page"]
# #     page()
# #     # st.title("🪪 About us")
# #     # st.write("Settings panel.")

