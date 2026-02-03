import json
import smtplib
import datetime
import pandas as pd
from fpdf import FPDF
from email.message import EmailMessage

def send_yearly_statement(user_email, csv_file):
    #Setup Date & Load Secrets
    now = datetime.datetime.now()
    #START DATE: January 1st of the current year
    start_of_year = datetime.datetime(now.year, 1, 1)
    
    try:
        with open("secret.json", 'r') as f:
            db = json.load(f)
    except FileNotFoundError:
        print("Error: secret.json not found.")
        return

    #Process Data
    try:
        df = pd.read_csv(csv_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        #Use start_of_year 
        yearly_data = df[df['timestamp'] >= start_of_year].copy()
        yearly_data = yearly_data.sort_values(by='timestamp', ascending=False)
    except Exception as e:
        print(f"Data Error: {e}")
        return

    #PDF Generation
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    #Header
    pdf.set_font("helvetica", 'B', 18)
    pdf.cell(0, 15, txt=f"M-PESA FULL STATEMENT - {now.year}", ln=True, align='C')
    pdf.set_font("helvetica", 'I', 10)
    pdf.cell(0, 5, txt=f"Reporting Period: {start_of_year.strftime('%d %b %Y')} to {now.strftime('%d %b %Y')}", ln=True, align='C')
    pdf.ln(10)

    #Table Header
    pdf.set_font("helvetica", 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    cols = ["Date & Time", "Transaction Details", "Tag", "Amount", "Fee", "Balance"]
    widths = [40, 55, 35, 35, 30, 40]
    
    for i in range(len(cols)):
        pdf.cell(widths[i], 8, cols[i], 1, 0 if i < len(cols)-1 else 1, 'C', True)

    #Table Rows
    pdf.set_font("helvetica", '', 8)
    for _, row in yearly_data.iterrows():
        if pdf.get_y() > 175:
            pdf.add_page()
            pdf.set_font("helvetica", 'B', 9)
            for i in range(len(cols)):
                pdf.cell(widths[i], 8, cols[i], 1, 0 if i < len(cols)-1 else 1, 'C', True)
            pdf.set_font("helvetica", '', 8)

        pdf.cell(widths[0], 7, row['timestamp'].strftime('%Y-%m-%d %H:%M'), 1)
        pdf.cell(widths[1], 7, f" {str(row['type'])[:50]}", 1)
        pdf.cell(widths[2], 7, str(row['tag']), 1)
        pdf.cell(widths[3], 7, f"{row['amount']:,.2f}", 1, 0, 'R')
        pdf.cell(widths[4], 7, f"{row['fee']:,.2f}", 1, 0, 'R')
        pdf.cell(widths[5], 7, f"{row['balance_after']:,.2f}", 1, 1, 'R')

    #Output PDF
    pdf_name = f"Mpesa_Statement_{now.strftime('%Y%m%d')}.pdf"
    pdf.output(pdf_name)

    #Email Transmission
    msg = EmailMessage()
    msg['Subject'] = f"M-PESA Annual Statement - {now.year}"
    msg['From'] = db.get("sender_email")
    msg['To'] = user_email
    msg.set_content(f"Hello {db.get('user_name')},\n\nAttached is your M-PESA transactions statement starting from January 1, {now.year}.")

    with open(pdf_name, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_name)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            #Match details from our 'secrets.json'
            server.login(db.get("sender_email"), db.get("sender_app_password"))
            server.send_message(msg)
        print(f"\n\033[92mSuccess: Mpesa statement sent to {user_email}\033[0m")
    except Exception as e:
        print(f"\n\033[91mSMTP Error: {e}\033[0m")