import logging
logging.getLogger("streamlit.runtime.caching").setLevel(logging.ERROR)
from sqlalchemy import create_engine,text
import pandas as pd
import streamlit as st
from urllib.parse import quote_plus
import os
import datetime
from datetime import datetime
from datetime import date
from pywinauto.application import Application
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)
from pathlib import Path
import shutil
import tempfile

# Function to open the Excel file
def open_file_or_folder(file_path,is_file=True):
    if not os.path.exists(file_path):
        st.warning(f"The file location do not exist, please contact the Strategic Planning Team.")
        return
    if is_file:
        os.startfile(file_path)
    else:
        folder_path = os.path.dirname(file_path)
        os.startfile(folder_path)
        # Attach to the Explorer window
        app = Application().connect(path='explorer.exe')
        # Wait for the window to be opened and focus on it
        app.top_window().set_focus()


def get_update_time(file_path):
    if os.path.exists(file_path):
        last_modified_time = os.path.getmtime(file_path)
        readable_update_time = datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M')
        return readable_update_time 
    return None

@st.cache_data(show_spinner=False, ttl="20m")
def get_reports(config_path, s_sheet_name, m_sheet_name, setting_sheet, gid):
    #Exclude folders
    exclude_df = pd.read_excel(config_path, sheet_name=setting_sheet, usecols=['Excluded Folder'])
    exclude_keywords = (
        exclude_df["Excluded Folder"]
        .dropna()                
        .astype(str)             
        .tolist()
    )
    #Structured reports
    s_report_list = pd.read_excel(config_path, sheet_name=s_sheet_name)
    s_report_list['Folder Path'] = s_report_list['Folder Path'].str.replace("*GID*", gid, regex=False)
    
    results = []

    for _, row in s_report_list.iterrows():
        folder = row["Folder Path"]
        pattern = row["Report Name Pattern"]
        
        for root, dirs, files in os.walk(folder): 
            if any(kw.lower() in root.replace(folder, "").lower() for kw in exclude_keywords):     
                continue

            for f in files:
                if f.startswith("~$"):  
                    continue
                if pattern.lower() in f.lower():  
                    file_path = os.path.join(root, f)
                    rel_folder = os.path.dirname(os.path.relpath(file_path, folder)).replace("\\", " | ")
                    results.append({
                        "Folder Path": folder,
                        "Report Name Pattern": pattern,
                        "Report Name": f,
                        "file_link": file_path,
                        "Extra Description": rel_folder,
                        "Update Time Raw": get_update_time(file_path)
                    })
    s_df = pd.DataFrame(results).merge(
        s_report_list, 
        on=["Folder Path", "Report Name Pattern"], 
        how='inner')
    #Mix reports
    m_report_list = pd.read_excel(config_path, sheet_name=m_sheet_name)
    m_report_list['file_link'] = m_report_list['file_link'].str.replace("*GID*", gid, regex=False)
    m_report_list['Update Time Raw'] = m_report_list['file_link'].apply(get_update_time)
    #Append
    report_list = pd.concat([s_df, m_report_list], ignore_index=True)
    #Update Warning
    threshold_df = pd.read_excel(config_path, sheet_name=setting_sheet, usecols=['Update Frequency', 'Threshold'])
    report_list = get_update_warning(report_list, threshold_df)
    
    return report_list
    

def get_update_warning(report_list, threshold):  
    report_list = report_list.merge(threshold, how='left', on='Update Frequency')
    # chuyển sang datetime, lỗi -> NaT
    report_list["Update Time Val"] = pd.to_datetime(report_list["Update Time Raw"], errors='coerce')
    
    # tính số ngày kể từ Update Time
    days_since_update = (pd.Timestamp('today') - report_list["Update Time Val"]).dt.days
    
    # cột Has Update Warning: NaT hoặc vượt Threshold
    report_list["Has Update Warning"] = (
        days_since_update.isna() | (days_since_update > report_list["Threshold"])
    ).map({True: "Yes", False: "No"})
    
    # cột Update Warning
    def format_warning(row):
        if pd.isna(row["Update Time Val"]):
            return "⚠️"
        text = row["Update Time Raw"]
        if (pd.Timestamp('today') - row["Update Time Val"]).days > row["Threshold"]:
            text += " ⚠️"
        return text
    
    report_list["Update Time"] = report_list.apply(format_warning, axis=1)
    
    return report_list

# def get_filter_options(df, columns, sep=","):
#     filter_options = {}
#     for col in columns:
#         if col not in df.columns:
#             return []
#         filter_options[col] = sorted(df[col].dropna().astype(str).str.split(sep).explode().str.strip().unique().tolist())
#     return filter_options

@st.cache_data(show_spinner=False, ttl="20m")
def get_unique_elements(series):
    elements = set()
    for item in series.dropna():
        parts = [x.strip() for x in str(item).split(',')]
        elements.update(parts)
    return sorted(elements)



def find_gid():
    base_path = Path("C:/Users")
    if not base_path.exists():
        st.error("Can not find your C:/Users folder.")
        return None
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name.isdigit(): 
            one_drive_path = folder / "OneDrive - Sony"
            if one_drive_path.exists() and one_drive_path.is_dir():
                return folder.name  
    st.warning("Can not find your OneDrive - Sony folder.")
    return None