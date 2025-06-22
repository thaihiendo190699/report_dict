from sqlalchemy import create_engine,text
import pandas as pd
import streamlit as st
from urllib.parse import quote_plus

@st.cache_data(show_spinner=False)
def get_db_connection(server_name,database,query,select_columns,column_types):
    # SQL Server connection string using Windows Authentication

    conn_str = (
        f"mssql+pyodbc://@{server_name}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )

    # Create the SQLAlchemy engine
    engine = create_engine(conn_str)
    df = pd.read_sql(query, engine)
    if len(select_columns)>0:
        df=df[select_columns]
    df=df.astype(column_types)
    return df

@st.cache_data(show_spinner=False,ttl="10m")
def get_db_connection_user_password(server_name,database,query,user_name,password,select_columns,column_types):
    # SQL Server connection string using Windows Authentication

    conn_str = (
        f"mssql+pyodbc://{user_name}:{quote_plus(password)}@{server_name}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    )

    # Create the SQLAlchemy engine
    engine = create_engine(conn_str)
    df = pd.read_sql(query, engine)
    df.reset_index(drop=True,inplace=True)
    if len(select_columns)>0:
        df=df[select_columns]
    df=df.astype(column_types)
    return df

@st.cache_data(show_spinner=False)
def get_source_link(config_file,worksheet_name,items_name):
    data=pd.read_excel(config_file,sheet_name=worksheet_name)
    print(data)
    print(data[data['Items']==items_name]['Link'])
    print(worksheet_name)
    print(items_name)
    return data[data['Items']==items_name]['Link'].values[0]


def validate_user(website_user,website_user_password,server_name=r'43.94.1.64\sqlserver01',database=r'Processing_Raw',server_user='usr_ci',server_user_password='Citool@123'):
   
    conn_str = (
        f"mssql+pyodbc://{server_user}:{quote_plus(server_user_password)}@{server_name}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    )

    # Create the SQLAlchemy engine
    engine = create_engine(conn_str)
    
    with engine.connect() as connection:
        result = connection.execute(
        text("SELECT dbo.payout_status_user_validation (:website_user,:website_user_password) AS is_valid"),
        {"website_user": website_user,
         "website_user_password":website_user_password}  # Parameter binding
        )
        # Fetch the first row
        row = result.fetchone()
        if row:
            is_valid = row[0]
            return is_valid
        else:
            return False
    
# print(validate_user('a','avas'))

