import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pywinauto import Application
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Function to open the Excel file
def open_file_or_folder(file_path, is_file=True):
    if is_file:
        os.startfile(file_path)
    else:
        folder_path = os.path.dirname(file_path)
        os.startfile(folder_path)
        app = Application().connect(path='explorer.exe')
        app.top_window().set_focus()

st.set_page_config(layout="wide")






st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem;
        }
    

}
    </style>
""", unsafe_allow_html=True)
st.header("Report Dictionary", divider=True)

config_link = r'D:\Project\Report_dictionary\Config.xlsx'
worksheet_name = 'Automate_refresh_report'

@st.cache_data(ttl=600,show_spinner=False)
def load_data_with_update_time(config_link, worksheet_name):
    report_list = pd.read_excel(config_link, sheet_name=worksheet_name)
    for idx, row in report_list.iterrows():
        file_link = row['file_link']
        last_modified_time = os.path.getmtime(file_link)
        readable_time = datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M')
        report_list.at[idx, 'Update time'] = readable_time
    
    return report_list

with st.spinner("Please wait..."):
    report_list = load_data_with_update_time(config_link, worksheet_name)

def get_unique_elements(series):
    elements = set()
    for item in series.dropna():
        parts = [x.strip() for x in str(item).split(',')]
        elements.update(parts)
    return sorted(elements)

# --- FILTER SECTION ---
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
with col1:
    search_tags = st.text_input("🔎", placeholder="Search...")
with col2:
    cate_filter = st.multiselect("Category", options=get_unique_elements(report_list["Category"]))
with col3:
    object_filter = st.multiselect("Focused Objects", options=get_unique_elements(report_list["Focused Objects"]))
with col4:
    users_filter = st.multiselect("Intended Users", options=get_unique_elements(report_list["Intended Users"]))


st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# --- FILTER LOGIC ---
filtered_report_list = report_list

if search_tags:
    filtered_report_list = filtered_report_list[
        filtered_report_list[['Report Name', 'Purpose']]
        .apply(lambda row: search_tags.lower() in ' '.join(row.astype(str)).lower(), axis=1)
    ]
if cate_filter:
    cate_pattern = '|'.join(cate_filter)
    filtered_report_list = filtered_report_list[filtered_report_list["Category"].str.contains(cate_pattern, case=False, na=False)]
if object_filter:
    object_pattern = '|'.join(object_filter)
    filtered_report_list = filtered_report_list[filtered_report_list["Focused Objects"].str.contains(object_pattern, case=False, na=False)]
if users_filter:
    users_pattern = '|'.join(users_filter)
    filtered_report_list = filtered_report_list[filtered_report_list["Intended Users"].str.contains(users_pattern, case=False, na=False)]

if filtered_report_list.empty:
    st.warning("⚠️ No matching reports found. Please adjust your filters.")
else:

    filtered_report_list = filtered_report_list[['Report Name', 'Purpose', 'Category', 'Focused Objects', 'Intended Users', 'Update Frequency', 'Update time', 'PIC', 'file_link']]
    gb = GridOptionsBuilder.from_dataframe(filtered_report_list)
    gb.configure_selection(selection_mode="single", use_checkbox=False)  # Không checkbox
    
    gb.configure_column("file_link", hide=True)  # ẨN cột Path
    # Wrap text cho các cột dài

    for col in filtered_report_list.columns:
        gb.configure_column(
            col,
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
            maxWidth=250,
            suppressSizeToFit=True,
            autoHeight=True
        )


    gb.configure_column("Report Name", pinned="left")
    grid_options = gb.build()

    # Tạo chỗ trống để update info sau
    info_placeholder = st.empty()   
    custom_css = {
    ".ag-header-cell": {
        "background-color": "#0d96fd !important",
        "color": "white !important",
        "font-weight": "bold !important"
    }
    }

    grid_response = AgGrid(filtered_report_list, gridOptions=grid_options, update_mode=GridUpdateMode.SELECTION_CHANGED, theme="balham", custom_css=custom_css)


    selected = grid_response["selected_rows"]

    if  selected is not None and len(selected) > 0:
        with info_placeholder.container():
            file_path = selected.iloc[0]['file_link']
            
            col1, col2, col3, _ = st.columns([3,1,1, 4], gap="small")
            with col1:
                st.write(f"Selected report: **{selected.iloc[0]['Report Name']}**")
            with col2:
                if st.button('Open File  ', key=f'file_{0}'):
                    open_file_or_folder(selected.iloc[0]['file_link'])
            with col3:
                if st.button('Open Folder', key=f'folder_{0}'):
                    open_file_or_folder(selected.iloc[0]['file_link'], False)

                    
    else:
        info_placeholder.info("Select a report row to open file/folder.")


    # Hiển thị số lượng báo cáo
    num_reports = filtered_report_list.shape[0]
    st.markdown(f"**Showing {num_reports} report(s).**")