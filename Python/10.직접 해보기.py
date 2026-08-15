import requests, smtplib, datetime
from email.mime.text import MIMEText
 
def send_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=5)
    resp.raise_for_status()
 
def send_email(smtp_user, smtp_pass, to_addr, message):
    msg = MIMEText(message)
    msg["Subject"] = "보안 알림 (텔레그램 실패로 대체 발송)"
    msg["From"] = smtp_user
    msg["To"] = to_addr
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
 
def notify_failover(message, config):
    try:
        send_telegram(config["tg_token"], config["tg_chat_id"], message)
        print("텔레그램 알림 전송 성공")
        return
    except Exception as e:
        print(f"텔레그램 실패: {e}, 이메일로 재시도")
    try:
        send_email(config["smtp_user"], config["smtp_pass"], config["to_addr"], message)
        print("이메일 알림 전송 성공")
        return
    except Exception as e:
        print(f"이메일도 실패: {e}, 로컬 파일에 기록")
    with open("missed_alerts.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} {message}\n")
