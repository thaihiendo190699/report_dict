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
def open_file_or_folder(path):
    os.startfile(path)



@st.cache_data(show_spinner=False, ttl="10m")
def get_unique_elements(series):
    elements = set()
    for item in series.dropna():
        parts = [x.strip() for x in str(item).split(',')]
        elements.update(parts)
    return sorted(elements)


@st.cache_data(show_spinner=False, ttl="10m")
def get_report(config_path, sheet_name):
    report_list = pd.read_excel(config_path, sheet_name=sheet_name)
    return report_list

