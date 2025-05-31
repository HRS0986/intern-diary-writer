import gradio as gr
from excel import ExcelHandler
from llm import refine_data_with_llm, generate_weekly_summary, generate_monthly_summary
from openai.types.chat import ChatCompletionContentPartTextParam
from record import DailyRecord

def load_excel():
    excel = ExcelHandler('../example.xlsx', ['February', 'March'])
    return excel

def process_records(selected_months):
    excel = load_excel()
    refined_records = {}
    
    for sheet in excel.sheet_names:
        if sheet not in selected_months:
            continue
            
        excel.change_sheet(sheet)
        
        # Read and refine daily records
        column_b = excel.read_column('B')
        records = [ChatCompletionContentPartTextParam(text=DailyRecord(record=record).model_dump(), type="text") for record in column_b]
        data = refine_data_with_llm(records)
        refined_records[sheet] = data
        excel.write_column('E', data)
        
        # Generate weekly summaries
        week_start_row = 2
        week_end_row = 6
        row_count = excel.get_data_rows_count('B')
        
        while week_start_row < row_count:
            summary = generate_weekly_summary(refined_records[sheet][week_start_row - 2:week_end_row - 1])
            excel.merge_cells_and_write(week_start_row, 'F', week_end_row, 'F', summary)
            week_start_row += 5
            week_end_row += 5
            
        # Generate monthly summary
        summary = generate_monthly_summary(refined_records[sheet])
        excel.merge_cells_and_write(2, 'G', excel.get_data_rows_count('B') + 1, 'G', summary)
    
    return "Reports generated successfully!", format_results(refined_records)

def format_results(refined_records):
    result = ""
    for month, records in refined_records.items():
        result += f"\n{month} Records:\n"
        for i, record in enumerate(records, 1):
            result += f"Day {i}: {record}\n"
    return result

def run_app(months):
    if not months:
        return "Please select at least one month!", ""
    
    try:
        return process_records(months.split(","))
    except Exception as e:
        return f"An error occurred: {str(e)}", ""

# Create Gradio interface
def create_interface():
    excel = load_excel()
    available_months = ",".join(excel.sheet_names)
    
    iface = gr.Interface(
        fn=run_app,
        inputs=[
            gr.Textbox(
                label="Enter months (comma-separated)", 
                placeholder="e.g. February,March",
                value=available_months
            )
        ],
        outputs=[
            gr.Textbox(label="Status"),
            gr.Textbox(label="Generated Reports", lines=10)
        ],
        title="Intern Diary Writer",
        description="Generate refined daily records and summaries from your intern diary",
        theme="default"
    )
    return iface

if __name__ == "__main__":
    iface = create_interface()
    iface.launch()