import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def aggregate_sum(rows: list[dict], column:str) -> float:
    if not rows:
        return 0.0
    return sum(float(row.get(column, 0)) for row in rows)


def group_count(rows: list[dict], column:str) -> dict:
    counts = {}
    for row in rows:
        key = row.get(column)
        if key:
            counts[key] = counts.get(key, 0) + 1
    return counts

def top_k_items(rows: list[dict], column: str, k: int = 5) -> dict:
    sorted_rows = sorted(rows, key=lambda x: float(x.get(column, 0)), reverse=True)
    top_k = sorted_rows[:k]
    return top_k





def email_sender(receiver:str,sub:str, body:str):
    

    # -----------------------------
    # Email configuration
    # -----------------------------
    sender_email = "shawkygamal150@gmail.com"
    sender_password = "gpzn vbli upsu uxzq"  # NOT your Gmail password!
    receiver_email = receiver
    subject = sub
    html_body = body

    # -----------------------------
    # Create the email
    # -----------------------------
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    # -----------------------------
    # Send the email
    # -----------------------------
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        

        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        print("Server quited")
        server.quit()

    