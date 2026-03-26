import gspread
import pandas as pd
import streamlit as st


class GoogleSheet:
    def __init__(self, document, sheet_name):
        credentials_info = dict(st.secrets["google_service_account"])
        self.gc = gspread.service_account_from_dict(credentials_info)
        self.sh = self.gc.open(document)
        self.sheet = self.sh.worksheet(sheet_name)

    def read_data(self, range):
        data = self.sheet.get(range)
        return data

    def read_data_by_uid(self, uid):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        filtered_data = df[df["id-usuario"] == uid]
        return filtered_data

    def write_data(self, range, values):
        self.sheet.update(range, values)

    def write_data_by_uid(self, uid, values):
        cell = self.sheet.find(uid)
        row_index = cell.row
        self.sheet.update(f"A{row_index}:E{row_index}", values)

    def get_last_row_range(self):
        last_row = len(self.sheet.get_all_values()) + 1
        range_start = f"A{last_row}"
        range_end = f"H{last_row}"
        return f"{range_start}:{range_end}"

    def get_all_values(self):
        return self.sheet.get_all_records()

    def get_members(self):
        table_members = self.get_all_values()
        df = pd.DataFrame(table_members)
        members = df["name"].tolist()
        return members