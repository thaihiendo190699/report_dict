

import logging
logging.getLogger("streamlit.runtime.caching").setLevel(logging.ERROR)
import streamlit as st
import pandas as pd
import numpy as np
import os
import re
from custom_function import get_unique_elements, get_report
from pywinauto import Application
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode,JsCode
from datetime import datetime, timedelta
from streamlit_cookies_manager import EncryptedCookieManager
import json
import warnings
warnings.filterwarnings("ignore")

def report_dictionary():

    # Khởi tạo cookie manager
    cookies = EncryptedCookieManager(
        prefix="myapp/",
        password="ngnhb",
    )

    if not cookies.ready():
        st.stop()


    # Load cookie lần đầu
    cookie_key = "filters"

    if "filters_loaded" not in st.session_state:
        if cookie_key in cookies:
            saved_filter = json.loads(cookies.get(cookie_key))
            st.session_state["users_filter"] = saved_filter.get("users_filter", [])
        else:
            st.session_state["users_filter"] = [] 
            x = {
                "users_filter": st.session_state["users_filter"]
                }
            cookies[cookie_key] = json.dumps(x)
        st.session_state["filters_loaded"] = True  # Đánh dấu đã load cookie
        
    # Layout
    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
            .block-container {
                padding-top: 1.5rem;
            },
            .stAlert {display: none;}
        
    }
        </style>
    """, unsafe_allow_html=True)

    st.title("Report Dictionary")
    # st.header("Report Dictionary", divider=True)

    #Load Report List
    with st.spinner("Loading..."):
        report_list = get_report()


    # Filter
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])
    with col1:
        search_tags = st.text_input("🔎", placeholder="Search...")
    with col2:
        topic_filter = st.multiselect("Topic", options=get_unique_elements(report_list["Topic"]))
    with col3:
        cate_filter = st.multiselect("Category", options=get_unique_elements(report_list["Category"]))
    with col4:
        object_filter = st.multiselect("Focused Objects", options=get_unique_elements(report_list["Focused Objects"]))
    with col5:
        users_filter = st.multiselect("Intended Users", 
                                  options=get_unique_elements(report_list["Intended Users"]), 
                                #   default=st.session_state.get("users_filter"),
                                  key="users_filter")
    with col6:
        type_filter = st.multiselect("Type", options=get_unique_elements(report_list["Type"]), default="Report")

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # Chỉ save cookie khi có thay đổi thật sự
    if cookie_key in cookies:
        if json.loads(cookies.get(cookie_key)).get("users_filter", []) != users_filter:
            cookies[cookie_key] = json.dumps({"users_filter": st.session_state["users_filter"]})
            cookies.save()

    # Filter Report List
    filtered_report_list = report_list

    if search_tags:
        # pattern = r"\b" + re.escape(search_tags.lower()) + r"\b"
        pattern = rf"(?<![A-Za-z]){re.escape(search_tags.lower())}(?![A-Za-z])"
        filtered_report_list = filtered_report_list[
            filtered_report_list[['Report Name', 'Purpose']]
            .apply(lambda row: bool(re.search(pattern, ' '.join(row.astype(str)).lower())), axis=1)
        ]
    if cate_filter:
        cate_pattern = '|'.join(cate_filter)
        filtered_report_list = filtered_report_list[(filtered_report_list["Category"].str.contains(cate_pattern, case=False, na=False)) | (filtered_report_list["Category"].str.upper() == "ALL")]
    if topic_filter:
        topic_pattern = '|'.join(topic_filter)
        filtered_report_list = filtered_report_list[filtered_report_list["Topic"].str.contains(topic_pattern, case=False, na=False)]
    if object_filter:
        object_pattern = '|'.join(object_filter)
        filtered_report_list = filtered_report_list[filtered_report_list["Focused Objects"].str.contains(object_pattern, case=False, na=False)]
    if users_filter:
        users_pattern = '|'.join(users_filter)
        filtered_report_list = filtered_report_list[filtered_report_list["Intended Users"].str.contains(users_pattern, case=False, na=False) | (filtered_report_list["Intended Users"].str.upper() == "ALL")]
    if type_filter:
        type_pattern = '|'.join(type_filter)
        filtered_report_list = filtered_report_list[filtered_report_list["Type"].str.contains(type_pattern, case=False, na=False)]
    if filtered_report_list.empty:
        st.warning("⚠️ No matching reports found. Please adjust your filters.")
    else:

        filtered_report_list = filtered_report_list[['Report Name', 'Purpose', 'Topic', 'Category', 'Focused Objects', 'Time Dimension', 'Update Frequency', 'PIC', 'file_link', 'folder_link']]
        gb = GridOptionsBuilder.from_dataframe(filtered_report_list)
        # gb.configure_default_column(resizable=True, flex=1)
        gb.configure_selection(selection_mode="single", use_checkbox=False)  # Không checkbox
        
        gb.configure_column("file_link", hide=True)  # ẨN cột Path
        gb.configure_column("folder_link", hide=True)  # ẨN cột Path
        # Wrap text cho các cột dài

        gb.configure_default_column(
            headerClass="bold-header",
            cellStyle={
                "display": "flex",
                "alignItems": "center",        
                "justifyContent": "flex-start", 
                "paddingLeft": "5px",
                "paddingRight": "5px", 
                "paddingTop": "5px",
                "paddingBottom": "5px",       
                "lineHeight": "1.2", 
                "whiteSpace": "normal"           
            },
            # maxWidth=300,
            flex=1,
            resizable=True,      
            # suppressSizeToFit=True,
            autoHeight=True
            )
                
        for col in filtered_report_list.columns:
            if col=='Report Name':
                gb.configure_column(
                    col,
                    # flex=2,
                    minWidth=200
                )
            elif col=='Purpose':
                gb.configure_column(
                    col,
                    # flex=2,
                    minWidth=300
                )
            else:
                gb.configure_column(
                    col,
                    # flex=1,
                    minWidth=120
                )

        gb.configure_column("Report Name", pinned="left")
        grid_options = gb.build()

        grid_options["onGridSizeChanged"] = JsCode("""
        function(params) {
            params.api.sizeColumnsToFit();
        }
        """)

        # Tạo chỗ trống để update info sau
        info_placeholder = st.empty()   
        custom_css = {
        ".ag-header-cell": {
            "background-color": "#0d96fd !important",
            "color": "white !important",
            "font-weight": "bold !important"
        }
        }

        grid_response=AgGrid(
            filtered_report_list,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme="balham",
            custom_css=custom_css,
            height=600,
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True
        )

        selected = grid_response["selected_rows"]

    # Select and Open Report
        if  selected is not None and len(selected) > 0:
            
            with info_placeholder.container():
                file_path = selected.iloc[0]['file_link']
                folder_path = selected.iloc[0]['folder_link']
                col1, col2, col3, _ = st.columns([2.5,1,1,3], gap="small")
                with col1:
                    st.write(f"Selected report: **{selected.iloc[0]['Report Name']}**")
                with col2:
                    st.markdown(
                            f'<a href="{file_path}" target="_blank"><button style="background-color: white; color: #5a5a5a; border: 0.5px solid #0d96fd;  border-radius: 6px; cursor: pointer;font-family: Arial, sans-serif;padding: 7px 20px;">Open File</button></a>',
                            unsafe_allow_html=True
                    )
                with col3:
                    st.markdown(
                            f'<a href="{folder_path}" target="_blank"><button style="background-color: white; color: #5a5a5a; border: 0.5px solid #0d96fd;  border-radius: 6px; cursor: pointer;font-family: Arial, sans-serif;padding: 7px 20px;">Open Folder</button></a>',
                            unsafe_allow_html=True
                    )
                        
        else:
            info_placeholder.info("Select a report row to open file/folder.")



    # Hiển thị số lượng báo cáo
        num_reports = filtered_report_list.shape[0]
        st.markdown(f"**Showing {num_reports} report(s).**")




