
import requests
import time
from bs4 import BeautifulSoup

# ======= بياناتك الحقيقية =======
TELEGRAM_TOKEN = "8470728931:AAHnOvnXxzAWVeIzXBnNgkvB0OSaOXI1NJg"
CHAT_ID = "6039682231"
URL_FORM = "https://minha.anem.dz/pre_rendez_vous"
NUM_CARTE_TRAVAIL = "431703000710"
NUM_CARTE_IDENTITE = "110031404000710008"
CHECK_INTERVAL = 60  # بالثواني

TEXT_NO_APPOINTMENT = "نعتذر منكم ! لا يوجد أي موعد متاح حاليا."

last_status = None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("خطأ في ارسال الرسالة:", e)

def check_appointments():
    global last_status
    try:
        session = requests.Session()
        form_data = {
            "num_carte_travail": NUM_CARTE_TRAVAIL,
            "num_carte_identite": NUM_CARTE_IDENTITE
        }
        response = session.post(URL_FORM, data=form_data)
        soup = BeautifulSoup(response.text, "html.parser")
        continue_link = soup.find("a", text="المواصلة")
        if continue_link:
            next_url = continue_link.get("href")
            response = session.get(next_url)
            soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()
        if TEXT_NO_APPOINTMENT not in page_text:
            status = "available"
        else:
            status = "not_available"
        if status != last_status:
            if status == "available":
                send_telegram_message("✅ تنبيه: تم فتح مواعيد في وكالة ميلة!\nرابط: " + URL_FORM)
            last_status = status
    except Exception as e:
        print("خطأ في فحص الصفحة:", e)

while True:
    check_appointments()
    time.sleep(CHECK_INTERVAL)
