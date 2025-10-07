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
from sqlalchemy import types
import pyodbc

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
def get_report():
    # report_list = pd.read_excel(config_path, sheet_name=sheet_name)
    report_list=get_data_from_server('SELECT * FROM dbo.REPORT_DICTIONARY_CONFIG')
    return report_list

database_name=r'Processing_Raw'

def record_dataframe_to_sql(dataframe_to_insert,dtype,table_name,database_name=database_name,if_exists='append',server_name=r'43.94.1.64\sqlserver01'):
    connection_string = f'mssql+pyodbc://{server_name}/{database_name}?charset=utf8mb4&driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    dataframe_to_insert.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False,dtype=dtype)
    engine.dispose()

def truncate_table(table_name,database_name=database_name,server_name=r'43.94.1.64\sqlserver01'):
    connection_string = f'mssql+pyodbc://{server_name}/{database_name}?charset=utf8mb4&driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    with engine.connect() as connection:
        connection.execute(text(f"TRUNCATE TABLE [{table_name}]"))
        connection.commit()

def get_data_from_server(query,driver=r'SQL Server',server=r'43.94.1.64\sqlserver01',database=database_name,username=r'user_stp1',password='Userstp@123'):
    with pyodbc.connect(f"DRIVER={driver};"
                        f"SERVER={server};"
                        f"DATABASE={database};"
                        f"UID={username};"
                        f"PWD={password};") as conn:
 
        # Load data into a pandas DataFrame
        df = pd.read_sql(query, conn)
    return df

def load_excel_file(file_path,sheet_name):
    data=pd.read_excel(io=file_path,sheet_name=sheet_name)
    return data

def upload_report_dictionary_config(file_path,sheet_name):
    data=load_excel_file(file_path,sheet_name)
    dtype={}
    for column in data.columns:
        dtype.setdefault(column,types.Unicode())
    table_name=r'REPORT_DICTIONARY_CONFIG'
    truncate_table(table_name)
    record_dataframe_to_sql(data,
                            dtype=dtype,
                            table_name=r'REPORT_DICTIONARY_CONFIG',
                            if_exists='append'
                            )

