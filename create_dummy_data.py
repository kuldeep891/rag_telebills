import os
import random
import datetime
from fpdf import FPDF

# Sample Data Pools
NAMES = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Davis", "Diana Evans"]
CITIES = ["Springfield", "Metropolis", "Gotham", "Star City", "Central City", "Coast City"]
STREETS = ["Maple St", "Oak Ave", "Pine Ln", "Cedar Blvd", "Elm St", "Birch Way"]

def generate_phone():
    return f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_date():
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + datetime.timedelta(days=random_days)

def create_bill(bill_id, output_dir="data"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Randomize Data
    name = random.choice(NAMES)
    city = random.choice(CITIES)
    street = random.choice(STREETS)
    address = f"{random.randint(100, 999)} {street}, {city}, IL {random.randint(60000, 69999)}"
    phone = generate_phone()
    email = f"{name.lower().replace(' ', '.')}@example.com"
    account_num = str(random.randint(100000000, 999999999))
    bill_date = generate_date()
    total_amount = round(random.uniform(20.0, 150.0), 2)
    
    # Header
    pdf.cell(200, 10, txt="TELEPHONE BILL STATEMENT", ln=1, align='C')
    pdf.ln(10)
    
    # Customer Info (PII)
    pdf.cell(200, 10, txt=f"Customer Name: {name}", ln=1)
    pdf.cell(200, 10, txt=f"Address: {address}", ln=1)
    pdf.cell(200, 10, txt=f"Phone Number: {phone}", ln=1)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=1)
    pdf.cell(200, 10, txt=f"Account Number: {account_num}", ln=1)
    pdf.ln(10)
    
    # Bill Details
    pdf.cell(200, 10, txt=f"Bill Date: {bill_date}", ln=1)
    pdf.cell(200, 10, txt=f"Total Amount Due: ${total_amount}", ln=1)
    pdf.ln(10)
    
    # Call Logs
    pdf.cell(200, 10, txt="Call Details:", ln=1)
    for i in range(1, 4):
        duration = random.randint(1, 60)
        cost = round(duration * 0.10, 2)
        call_date = bill_date - datetime.timedelta(days=random.randint(0, 20))
        pdf.cell(200, 10, txt=f"{i}. {call_date} - {generate_phone()} - {duration} mins - ${cost}", ln=1)
    
    # Save
    filename = f"bill_{bill_id}_{name.replace(' ', '_')}.pdf"
    output_path = os.path.join(output_dir, filename)
    os.makedirs(output_dir, exist_ok=True)
    pdf.output(output_path)
    print(f"Created bill: {output_path}")

def generate_bulk_data(count=5):
    print(f"Generating {count} dummy bills...")
    for i in range(count):
        create_bill(i+1)
    print("Done!")

if __name__ == "__main__":
    generate_bulk_data(5)
