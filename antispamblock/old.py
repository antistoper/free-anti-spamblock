import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import time
import random
import urllib3
import requests
import json
import os

import asyncio
import aiosmtplib

import termcolor

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
with open("sets/emails.json") as emails_file:
    senders = json.load(emails_file)

receivers = ['abuse@telegram.org', 'support@telegram.org']

subject = "Request to Remove Spam Block"
enum_ = 10000
contact = input("юз: ")
body = f"""
Hello,

My name is {contact}, and I have encountered a block on my messages in Telegram due to suspicion of spam. I want to clarify that I use Telegram solely for communicating with friends, colleagues, and for personal or work-related purposes.

If any of my actions caused suspicion, it was unintentional. I strive to follow Telegram's rules and avoid activities that could be perceived as spam.

Please help me resolve this issue and, if possible, remove the block. I am ready to provide additional information if needed.

Thank you for your time and assistance!

Best regards,
{contact}"""

bad = 0

async def send_request(sent_emails):
    global bad
    sender_email, sender_password = random.choice(list(senders.items()))
    if sender_email.endswith("@mail.ru") or sender_email.endswith("@xmail.ru") or sender_email.endswith("@vk.com"): server = aiosmtplib.SMTP(hostname="smtp.mail.ru", port=587)
    elif sender_email.endswith("@gmail.com"): server = aiosmtplib.SMTP(hostname="smtp.gmail.com", port=587)

    try:
        await server.connect()
        await server.login(sender_email, sender_password)

        receiver = random.choice(receivers)
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver
        msg.set_content(body)
        await server.send_message(msg)
        text = termcolor.colored(f"Запрос №{sent_emails + 1} отправлен на {receiver} от {sender_email}!", "blue")
        print(text)
    except Exception as exc:
        bad += 1
        text = termcolor.colored(f"Запрос №{sent_emails + 1} от {sender_email} не был отправлен", "red")
        print(text)
    server.close()

async def main():
    gather_list = []

    for sent in range(1, enum_):
        gather_list.append(send_request(sent))

    await asyncio.gather(*gather_list)

asyncio.run(main())
print("Успешных: ", enum_ - bad)