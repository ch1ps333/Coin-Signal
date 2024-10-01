from fpdf import FPDF
import asyncio
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datebase.user import get_all_users, reset_signals_history
from dotenv import load_dotenv
from os import getenv, remove

load_dotenv()

def create_report(text, tg_id):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        
        lines = text.split('\n')
        for line in lines:
            pdf.cell(0, 10, txt=line, ln=True, align='C')

        pdf_file_path = f"Report_{tg_id}.pdf"
        pdf.output(pdf_file_path)
        return pdf_file_path
    except Exception as err:
        print(f"Error creating PDF: {err}")
        return False

    
async def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password, pdf_file):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_file, 'rb') as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_file)
        msg.attach(pdf_attachment)

    try:
        async with SMTP(hostname=smtp_server, port=smtp_port, start_tls=True) as server:
            await server.login(login, password)
            await server.send_message(msg)
            print(f"Email sent to {to_email} successfully!")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
    
async def reports_handle():
    users = await get_all_users()
    if users:
        for user in users:
            report = create_report(user.signals_history, user.tg_id)
            if report:
                await send_email(
                    "Crypto Signals report", 
                    "Your report is ready.", 
                    user.email,
                    getenv("EMAIL_LOGIN"), 
                    "smtp.gmail.com", 
                    587, 
                    getenv("EMAIL_LOGIN"), 
                    getenv("EMAIL_PASSWORD"), 
                    report
                )
                remove(report)
        await reset_signals_history()

if __name__ == "__main__":
    asyncio.run(reports_handle())
