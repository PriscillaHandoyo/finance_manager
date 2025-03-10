import csv
import re
from time import strptime
import gspread
from operator import itemgetter
from datetime import datetime
import time

file = "/Users/priscillahandoyo/Documents/Project/finance_manager/Mar2024-Mar2025.csv"
output_file = "/Users/priscillahandoyo/Documents/Project/finance_manager/bank_statement_sorted.csv"

# Define categories and their keywords
categories = {
    'Allowance': ["IRWAN"],
    'Eating out & Takeaway': ["BWS","CRUNCH", "CocaColaEPP", "EzyMart", "LANZHOU", "LIBRARY", "MCDONALDS", "Peppercorn", "Rolld", "ESPRESSO", "WORLD", "BAVARIAN", "RESCH", "UBER *EATS", "UBER EATS*", "YORI", "YUN", "gnibl"],
    'Entertainment': ["EVENT", "MASHTIX", "Mary's", "Qudos", "STONEWALL", "UNIVERSAL", "UPPERROOM"],
    'Fees': ["International"],
    'Groceires': ["ALDI", "CHEMIST", "COLES", "MIRACLE", "MART", "TSG", "WOOLWORTHS"],
    'Laundry': ["LAUNDRY"],
    'Refund': ["Refund", "Return"],
    'Subscriptions': ["ABLEAPP", "AMZNPRIMEAU", "APPLE", "VERITAS ENGINEERING", "YouTube", "OPENAI", "PRIMEVIDEO", "STAN.COM.AU", "Vodafone"],
    'Shopping': ["AMAZON", "COTTON", "Downtown", "KMART", "MACSHOP", "UGG"],
    'Transport': ["TFNSW", "TRANSPORTFORNSW", "UBER* TRIP"],
    'Transfers': ["Fast", "Transfer"]
}

# Categorize transactions
def categorize_transaction(desc):
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in desc:
                return category
    return 'Other'

# Extract month from date string
def extract_month(date_str):
    date_obj = datetime.strptime(date_str, '%d/%m/%Y') # strptime: string to datetime
    return date_obj.strftime('%B') # strftime: datetime to string

# Store transactions by month
transactions_by_month = {}

def commbank(file):
    sum = 0
    transactions = []  # Initialize transactions list inside the function

    # Open the original file
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader: 
            date = row[0]
            amount = float(row[1].replace('"', '')) # Remove quotes 
            name = row[2].replace('"', '') # Remove quotes
            balance = float(row[3].replace('"', '')) # Remove quotes

            sum += amount

            # Categorize the transaction
            category = categorize_transaction(name)

            # Extract month from the date
            month = extract_month(date)

            # Create a transaction tuple 
            transaction = (date, name, amount, category)

            # Add to the 'month' dictionary
            if month not in transactions_by_month:
                transactions_by_month[month] = []

            transactions_by_month[month].append(transaction)
            print(transaction)
            transactions.append(transaction)

    return transactions, sum

# Call the commbank function and get transactions and sum
transactions, total_sum = commbank(file)
print(f"Total sum of transactions: {total_sum}")

# Sort the transactions by description (index 2)
sorted_transactions = sorted(transactions, key=itemgetter(2))

# Write the sorted transactions to a new CSV file 
with open(output_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for transaction in sorted_transactions:
        csv_writer.writerow(transaction)

# Open the google spreadsheet
sa = gspread.service_account()
sh = sa.open_by_url("https://docs.google.com/spreadsheets/d/1oyPR2FpFYEpcA-VZ8KrWcC38l5gheV5268LRqolrZwM/edit")

# Get a worksheet by name (case-insensitive)
def get_worksheet_by_name(sheet, name):
    # List all worksheets
    worksheets = sheet.worksheets()
    for ws in worksheets:
        if ws.title.lower() == name.lower():
            return ws
    return None

# Get the current month
month = datetime.now().strftime('%B')

# Replace the current month-specific code with this loop over all months
for month, month_transactions in transactions_by_month.items():
    # Try to access the worksheet for this month
    wks = get_worksheet_by_name(sh, month)
    
    if wks is None:
        # If the worksheet doesn't exist, create it
        wks = sh.add_worksheet(title=month, rows="100", cols="20")
        print(f"Created new worksheet: {month}")
    else:
        print(f"Found existing worksheet: {month}")
    
    # Write the header
    wks.update(values=[['Date', 'Description', 'Amount', 'Category']], range_name='A1')
    
    # Prepare all the data as a list of lists
    all_rows = [list(transaction) for transaction in month_transactions]
    
    # Only proceed if there are transactions for this month
    if all_rows:
        # Use batch update with the correct argument order
        wks.update(values=all_rows, range_name=f'A2:D{len(all_rows) + 1}')
        print(f"Updated {len(all_rows)} transactions for {month}")
    else:
        print(f"No transactions found for {month}")
    
    # Add a small delay between updating different worksheets to avoid hitting API limits
    time.sleep(1)