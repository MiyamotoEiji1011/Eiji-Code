import pandas as pd

def set_sheet(sheet_name):
    try:
        # Excelファイルを読み込む際にエンジンを指定
        xls = pd.ExcelFile('todo_list.xlsx', engine='openpyxl')
        if sheet_name in xls.sheet_names:
            global current_sheet_name
            current_sheet_name = sheet_name
            print(f'Sheet set to {sheet_name}')
        else:
            print(f'Sheet "{sheet_name}" not found.')
    except Exception as e:
        print(f'Error: {str(e)}')

