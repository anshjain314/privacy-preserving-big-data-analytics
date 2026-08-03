from faker import Faker
import random
import string

fake = Faker("en_IN")


# -----------------------------------------------------
# PERSON
# -----------------------------------------------------

def person_name():
    return fake.name()


# -----------------------------------------------------
# EMAIL
# -----------------------------------------------------

def email():
    domains = [
        "gmail.com",
        "yahoo.com",
        "outlook.com",
        "company.com",
        "hotmail.com"
    ]

    username = fake.user_name()

    return f"{username}@{random.choice(domains)}"


# -----------------------------------------------------
# PHONE
# -----------------------------------------------------

def phone():
    return str(random.randint(6000000000, 9999999999))


# -----------------------------------------------------
# ADDRESS
# -----------------------------------------------------

def address():
    return fake.address().replace("\n", ", ")


# -----------------------------------------------------
# PAN
# -----------------------------------------------------

def pan():
    letters = ''.join(random.choices(string.ascii_uppercase, k=5))
    digits = ''.join(random.choices(string.digits, k=4))
    last = random.choice(string.ascii_uppercase)

    return letters + digits + last


# -----------------------------------------------------
# AADHAAR
# -----------------------------------------------------

def aadhaar():
    return ''.join(random.choices(string.digits, k=12))


# -----------------------------------------------------
# PASSPORT
# -----------------------------------------------------

def passport():
    return (
        random.choice(string.ascii_uppercase)
        + ''.join(random.choices(string.digits, k=7))
    )


# -----------------------------------------------------
# BANK ACCOUNT
# -----------------------------------------------------

def account_number():
    return ''.join(random.choices(string.digits, k=12))


# -----------------------------------------------------
# CREDIT / DEBIT CARD
# -----------------------------------------------------

def card_number():
    return ''.join(random.choices(string.digits, k=16))


# -----------------------------------------------------
# AGE
# -----------------------------------------------------

def age():
    return random.randint(18, 85)


# -----------------------------------------------------
# DATE OF BIRTH
# -----------------------------------------------------

def dob():
    return fake.date_of_birth(minimum_age=18, maximum_age=85).strftime("%Y-%m-%d")


# -----------------------------------------------------
# SALARY
# -----------------------------------------------------

def salary():
    return random.randint(15000, 300000)


# -----------------------------------------------------
# CITY
# -----------------------------------------------------

def city():
    return fake.city()


# -----------------------------------------------------
# STATE
# -----------------------------------------------------

def state():
    return fake.state()


# -----------------------------------------------------
# COUNTRY
# -----------------------------------------------------

def country():
    return fake.country()


# -----------------------------------------------------
# SAFE FIELDS
# -----------------------------------------------------

def loan_status():
    return random.choice([
        "Approved",
        "Pending",
        "Rejected"
    ])


def account_type():
    return random.choice([
        "Savings",
        "Current",
        "Salary",
        "Business"
    ])


def customer_segment():
    return random.choice([
        "Retail",
        "Corporate",
        "Premium",
        "Gold"
    ])


def credit_score():
    return random.randint(300, 900)


def interest_rate():
    return round(random.uniform(5.5, 15.0), 2)


def transaction_count():
    return random.randint(1, 500)


def balance():
    return round(random.uniform(0, 5000000), 2)


def loan_amount():
    return round(random.uniform(50000, 5000000), 2)


def risk_score():
    return round(random.uniform(0, 100), 2)


def branch():
    return random.choice([
        "Bangalore",
        "Mumbai",
        "Delhi",
        "Hyderabad",
        "Chennai",
        "Pune"
    ])


def department():
    return random.choice([
        "HR",
        "Finance",
        "Sales",
        "Marketing",
        "Operations",
        "IT"
    ])


def designation():
    return random.choice([
        "Manager",
        "Engineer",
        "Analyst",
        "Developer",
        "Executive",
        "Consultant"
    ])


def semester():
    return random.randint(1, 8)


def cgpa():
    return round(random.uniform(5.0, 10.0), 2)


def order_id():
    return "ORD" + ''.join(random.choices(string.digits, k=6))


def invoice_number():
    return "INV" + ''.join(random.choices(string.digits, k=6))


def product_name():
    return random.choice([
        "Laptop",
        "Phone",
        "Television",
        "Tablet",
        "Headphones",
        "Printer"
    ])


def category():
    return random.choice([
        "Electronics",
        "Furniture",
        "Fashion",
        "Books",
        "Healthcare"
    ])


# -----------------------------------------------------
# MASTER GENERATOR MAP
# -----------------------------------------------------

GENERATORS = {

    "PERSON_NAME": person_name,

    "EMAIL": email,

    "PHONE": phone,

    "ADDRESS": address,

    "PAN": pan,

    "AADHAAR": aadhaar,

    "PASSPORT": passport,

    "ACCOUNT": account_number,

    "CARD": card_number,

    "AGE": age,

    "DOB": dob,

    "SALARY": salary,

    "CITY": city,

    "STATE": state,

    "COUNTRY": country,

    "SAFE": {
        "Loan_Status": loan_status,
        "Account_Type": account_type,
        "Customer_Segment": customer_segment,
        "Credit_Score": credit_score,
        "Interest_Rate": interest_rate,
        "Transaction_Count": transaction_count,
        "Balance": balance,
        "Loan_Amount": loan_amount,
        "Risk_Score": risk_score,
        "Branch": branch,
        "Department": department,
        "Designation": designation,
        "Semester": semester,
        "CGPA": cgpa,
        "Order_ID": order_id,
        "Invoice_Number": invoice_number,
        "Product_Name": product_name,
        "Category": category
    }

}