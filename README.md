# Intern Diary Writer

## Usage

Use the example.xlsx files as the template for the diary. The diary will be written in the same format as the example.xlsx file. Duplicate the existing sheet and rename it for each new month. You just have to fill the Date and Description columns only.

### Installation

1. Clone the repository
```bash
git clone https://github.com/HRS0986/intern-diary-writer.git
```

2. Install the dependencies
```bash
cd intern-diary-writer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application
```bash
python main.py
# Enter Sheet Names You Want To Write Diary
```

### Customizing Default Prompts
Prompts are saved in `prompts.yaml` file. You can customize the prompts by editing the file:

* **Daily Report**
  * Purpose: Refine daily records

* **Weekly Report**
  * Purpose: Generate weekly report from daily reports

* **Monthly Report**
  * Purpose: Generate monthly report from weekly reports