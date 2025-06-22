import streamlit as st
import pandas as pd
import numpy as np
import os
from custom_function import get_source_link
from datetime import datetime
from pywinauto import Application



# Function to open the Excel file
def open_file_or_folder(file_path,is_file=True):
    if is_file:
        os.startfile(file_path)
    else:
        folder_path = os.path.dirname(file_path)
        os.startfile(folder_path)
        # Attach to the Explorer window
        app = Application().connect(path='explorer.exe')
    
    #    Wait for the window to be opened and focus on it
        app.top_window().set_focus()

st.set_page_config(layout="wide")
st.header("Report Dictionary", divider=True)


# # Thêm CSS để giới hạn độ rộng
# st.markdown("""
#     <style>
#         .main .block-container {
#             max-width: 80%;
#             margin: 0 auto;
#         }
#     </style>
# """, unsafe_allow_html=True)

# st.markdown(""" 
#              <p style='font-size:15px;'>
#             This is centralized reference that provides detailed information about the reports
#          used within an organization. It includes descriptions of the reports, their purpose, the data sources they use, definitions of key fields, and any business rules applied. The report dictionary helps ensure consistency and clarity, making it easier for users to understand and interpret the data in reports. It serves as a valuable tool for both report creators and users, promoting accurate communication and effective decision-making
#              </p>""",unsafe_allow_html=True)

config_link=r'D:\Project\Report_dictionary\Config.xlsx'
worksheet_name='Automate_refresh_report'
report_list=pd.read_excel(config_link,sheet_name=worksheet_name)

reports_folder=get_source_link(config_link,'Source_link','Automatic_report_folder')

for roots,subdirectories,files in os.walk(reports_folder):
    for file in files:
        if not 'Archive' in roots and 'Draft' not in roots and file in report_list['Report Name'].tolist():
            file_link=os.path.join(roots,file)
            # file_link=file_link.replace(os.sep,'/')
            report_list.loc[report_list['Report Name']==file,'file_link']=file_link
            # safe_path = urllib.parse.quote(file_path)
            # report_list['Open Directly']=f'<a href="file:///{safe_path}" target="_blank">Open Directly</a>'
            last_modified_time = os.path.getmtime(os.path.join(roots,file))
            readable_time = datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M')
            report_list.loc[report_list['Report Name']==file,'Update time']=readable_time 

# st.markdown(
#     """
#     <style>
#     .medium-font {
#         font-size:20px !important;
#         font-weight: bold;
#     }
#     </style>
#     """, unsafe_allow_html=True
# )            
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
    object_filter = st.multiselect("Focused Object", options=get_unique_elements(report_list["Focused Object"]))
with col4:
    users_filter = st.multiselect("Intended Users", options=get_unique_elements(report_list["Intended Users"]))

# --- SPACER between filter & table ---
st.markdown("### ")  # Adds ~1 empty line of space
# or for more precise:
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)




    # Thêm filter khác tương tự

# --- SIDEBAR ---
# st.sidebar.header("Search")
# search_tags = st.sidebar.text_input("What are you looking for?")
# cate_filter = st.sidebar.multiselect("Category", options=get_unique_elements(report_list["Category"]))
# object_filter = st.sidebar.multiselect("Focused Object", options=get_unique_elements(report_list["Focused Object"]))
# users_filter = st.sidebar.multiselect("Intended Users", options=get_unique_elements(report_list["Intended Users"]))


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
    filtered_report_list = filtered_report_list[filtered_report_list["Focused Object"].str.contains(object_pattern, case=False, na=False)]
if users_filter:
    users_pattern = '|'.join(users_filter)
    filtered_report_list = filtered_report_list[filtered_report_list["Intended Users"].str.contains(users_pattern, case=False, na=False)]

if filtered_report_list.empty:
    st.warning("⚠️ No matching reports found. Please adjust your filters.")


# search_query = st.text_input("Intended Users", "")

# if search_query:
#     filtered_report_list = report_list[report_list['Intended Users'].str.contains(search_query, case=False, na=False)]
# else:
#     filtered_report_list = report_list

# Display headers
col1, col2, col3, col4, col5,col6,col7,col8, col9, col10 = st.columns([2, 3, 1, 1, 1, 1, 1, 1, 1,1],vertical_alignment='center')

with col1:
    # st.caption('Report Name')
    st.markdown('<p class="medium-font">Report Name</p>',unsafe_allow_html=True)

with col2:
    # st.caption('Purpose')
    st.markdown('<p class="medium-font">Purpose</p>',unsafe_allow_html=True)

with col3:
    # st.caption('Category')
    st.markdown('<p class="medium-font">Category</p>',unsafe_allow_html=True)

with col4:
    # st.caption('Object')
    st.markdown('<p class="medium-font">Focused Object</p>',unsafe_allow_html=True)

with col5:
    # st.caption('Intended Users')
    st.markdown('<p class="medium-font">Intended Users</p>',unsafe_allow_html=True)

with col6:
    # st.caption('Update Frequency')
    st.markdown('<p class="medium-font">Update Frequency</p>',unsafe_allow_html=True)

with col7:
    # st.caption('Last update')
    st.markdown('<p class="medium-font">Last update</p>',unsafe_allow_html=True)

with col8:
    # st.caption('Last update')
    st.markdown('<p class="medium-font">PIC</p>',unsafe_allow_html=True)



with col9:
    st.caption('')

with col10:
    st.caption('')

# Create a button for each row in the DataFrame
print(filtered_report_list)
for index, row in filtered_report_list.iterrows():
    col1, col2, col3,col4,col5,col6,col7,col8, col9, col10 = st.columns([2, 3, 1, 1, 1,1,1,1,1,1],vertical_alignment='center')
    
    with col1:
        st.write(f"{row['Report Name']}")
    
    with col2:
        st.write(f"{row['Purpose']}")
    
    with col3:
        st.write(f"{row['Category']}")

    with col4:
        st.write(f"{row['Focused Object']}")

    with col5:
        st.write(f"{row['Intended Users']}")
    
    with col6:
        st.write(f"{row['Update Frequency']}")

    with col7:
        st.write(f"{row['Update time']}")
    
    with col8:
        st.write(f"{row['PIC']}")


    # with col9:
    #     # Button to open the file
    #     if st.button('Open', key=f'file_{index}'):
    #         open_file_or_folder(row['file_link'])

    # with col10:   
    #     if st.button('Open Folder', key=f'folder_{index}'):
    #         open_file_or_folder(row['file_link'],False)
    with col9:
        if st.button('Open', key=f'file_{index}'):
            open_file_or_folder(row['file_link'])

        if st.button('Open Folder', key=f'folder_{index}'):
            open_file_or_folder(row['file_link'], False)

# st.dataframe(filtered_report_list[['Report Name', 'Purpose', 'Category', 'Focused Object', 'Intended Users', 'Update Frequency', 'Update time', 'PIC', 'Note']])

# for index, row in filtered_report_list.iterrows():
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button('Open Directly', key=f'file_{index}'):
#             open_file_or_folder(row['file_link'])
#     with col2:
#         if st.button('Open Folder', key=f'folder_{index}'):
#             open_file_or_folder(row['file_link'], False)




