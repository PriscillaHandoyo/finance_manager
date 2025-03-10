# Finance Manager Automator

## Overview
Finance Manager Automator is a Python-based tool designed to automate the process of generating finance reports in Google Sheets. By uploading a bank statement, this tool processes transactions and updates a Google Sheets document using the Google Sheets API.

Based from [Internet Made Coder - How I AUTOMATE my FINANCES USING PYTHON](https://www.youtube.com/watch?v=IbdgcUqWSeo)

## Features
- Parses bank statements to extract transactions.
- Categorizes and organizes financial data.
- Automatically updates a Google Sheets document with the processed data.
- Provides insights into income, expenses, and financial trends.

## Requirements
Before running the Finance Manager Automator, ensure you have the following installed:

- Python 3.x
- Required dependencies (see `requirements.txt`)
- A Google Cloud project with Google Sheets API enabled
- Service account credentials (JSON file) with appropriate permissions to edit Google Sheets

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/finance-manager.git
   cd finance-manager
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up Google Sheets API:
   - Create a Google Cloud project.
   - Enable the Google Sheets API.
   - Create a service account and download the JSON credentials file.
   - Share access to your Google Sheets document with the service account email.

## Usage
1. Place your bank statement file (CSV or other supported formats) in the `data/` directory.
2. Run the script:
   ```sh
   python main.py --sheet-id YOUR_SHEET_ID --credentials path/to/credentials.json
   ```
3. The processed data will be automatically uploaded to your Google Sheets document.

## Example Google Sheets
Your financial report will be formatted similar to this example:
[Google Sheets Example](https://docs.google.com/spreadsheets/d/1oyPR2FpFYEpcA-VZ8KrWcC38l5gheV5268LRqolrZwM/edit?usp=sharing)

## Configuration
- Modify the `config.json` file to customize transaction categories, column mappings, or data processing rules.

## Troubleshooting
- Ensure your credentials JSON file is correctly configured.
- Verify that the Google Sheets document is shared with the service account email.
- Check for missing dependencies by running:
  ```sh
  pip list
  ```
- If the script fails, inspect the log files in the `logs/` directory for error messages.

## License
This project is licensed under the MIT License.

## Contributing
Feel free to submit issues or pull requests to enhance functionality or improve the reporting process.

