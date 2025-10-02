from custom_function import upload_report_dictionary_config,get_data_from_server

# upload_report_dictionary_config('Report_Dictionary.xlsx','Reports')

data=get_data_from_server('SELECT * FROM dbo.REPORT_DICTIONARY_CONFIG')
print(data)
