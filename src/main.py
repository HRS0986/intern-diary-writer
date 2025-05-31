import os
from dotenv import load_dotenv
from excel import ExcelHandler
from llm import refine_data_with_llm, generate_weekly_summary
from record import DailyRecord
from openai.types.chat import ChatCompletionContentPartTextParam
import openai

load_dotenv()

print(*openai.models.list(), sep="\n")

excel = ExcelHandler('../example.xlsx', ['February', 'March'])
refined_records = {}

def create_weekly_summary():
    for sheet in excel.sheet_names:
        excel.change_sheet(sheet)
        week_number = 1
        week_start_row = 2
        week_end_row = 6
        row_count = excel.get_data_rows_count('B')
        while week_start_row < row_count:
            content = refined_records[sheet][week_start_row - 2:week_end_row - 1]
            summary = generate_weekly_summary(content)
            excel.merge_cells_and_write(week_start_row, 'F', week_end_row, 'F', summary)
            week_number += 1
            week_start_row += 5
            week_end_row += 5

def generate_monthly_summary():
    for sheet in excel.sheet_names:
        excel.change_sheet(sheet)
        content = refined_records[sheet]
        summary = generate_weekly_summary(content)
        excel.merge_cells_and_write(2, 'G', excel.get_data_rows_count('B') + 1, 'G', summary)

def refine_daily_records(months: list[str]):
    for sheet in excel.sheet_names:
        if sheet not in months: continue
        excel.change_sheet(sheet)
        column_b = excel.read_column('B')
        records: list[ChatCompletionContentPartTextParam] = [ChatCompletionContentPartTextParam(text=DailyRecord(record=record).model_dump(), type="text") for record in column_b]
        data = refine_data_with_llm(records)
        refined_records[sheet] = data
        excel.write_column('E', data)

# if __name__ == '__main__':
    # month_names = input("Enter months to generate reports (separate by space): ").strip().split()
    # refine_daily_records(month_names)
    # create_weekly_summary()
    # generate_monthly_summary()