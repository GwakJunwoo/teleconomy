import pandas as pd
from EconomicCalendar import EconomicCalendarData
from message import format_alert_messages
from telegram import send_telegram_alerts
import os

def make_mock_df():
    # KST 기준 mock 데이터
    data = [
        {"시간": "01:00 PM", "KST_DATETIME": "2025-07-14 13:00:00", "국가": "Japan", "국가코드": "JP", "지표명": "GDP", "레퍼런스": "Q2", "발표치": "", "예상치": "1.0%", "예측치": "1.1%", "이전치": "0.9%"},
        {"시간": "02:00 PM", "KST_DATETIME": "2025-07-14 14:00:00", "국가": "Japan", "국가코드": "JP", "지표명": "CPI", "레퍼런스": "JUN", "발표치": "", "예상치": "2.0%", "예측치": "2.1%", "이전치": "1.9%"},
    ]
    return pd.DataFrame(data)

def make_mock_new_df():
    # 두 번째 데이터에 발표치가 채워진 상황
    data = [
        {"시간": "01:00 PM", "KST_DATETIME": "2025-07-14 13:00:00", "국가": "Japan", "국가코드": "JP", "지표명": "GDP", "레퍼런스": "Q2", "발표치": "", "예상치": "1.0%", "예측치": "1.1%", "이전치": "0.9%"},
        {"시간": "02:00 PM", "KST_DATETIME": "2025-07-14 14:00:00", "국가": "Japan", "국가코드": "JP", "지표명": "CPI", "레퍼런스": "JUN", "발표치": "2.2%", "예상치": "2.0%", "예측치": "2.1%", "이전치": "1.9%"},
    ]
    return pd.DataFrame(data)

def test_alert_logic():
    old_df = make_mock_df()
    new_df = make_mock_new_df()
    ec = EconomicCalendarData(old_df)
    new_alerts = ec.compare_and_alert(new_df)
    print("[TEST] 신규 알림 감지 결과:")
    print(new_alerts)
    if not new_alerts.empty:
        messages = format_alert_messages(new_alerts)
        print("[TEST] 메시지 포맷 결과:")
        for msg in messages:
            print(msg)
        # 실제 텔레그램 전송
        BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8083119806:AAHbMtmBORqBn_Co_JywKjcAqrsL1jNd46U')
        CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1002424388234')
        send_telegram_alerts(messages, BOT_TOKEN, CHAT_ID)
        print("[TEST] 텔레그램 전송 완료")
    else:
        print("[TEST] 신규 알림 없음")

if __name__ == "__main__":
    test_alert_logic()
