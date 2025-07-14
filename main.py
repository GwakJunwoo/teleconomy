
from CalendarCrawler import get_calendar
from EconomicCalendar import EconomicCalendarData
from Timer import timer_until_window

from message import format_alert_messages
from telegram import send_telegram_alerts
import pandas as pd
import os
import time

# 환경 변수 또는 직접 입력
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '여기에_봇_토큰')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '여기에_채팅_ID')


# 최초 데이터 적재 및 타겟 시간 계산
initial = EconomicCalendarData(get_calendar())

def get_next_target_time(df):
    now = pd.Timestamp.now(tz=None)
    # KST_DATETIME이 현재 이후인 것 중 가장 빠른 시간
    future = df[df['KST_DATETIME'].notna() & (df['KST_DATETIME'] > now)]
    if not future.empty:
        return future['KST_DATETIME'].min()
    return None


def crawl_and_alert_and_reschedule():
    global initial
    # 최신 데이터 크롤링
    new_df = get_calendar()
    # 신규 알림 감지
    new_alerts = initial.compare_and_alert(new_df)
    if not new_alerts.empty:
        # 메시지 생성 및 전송
        messages = format_alert_messages(new_alerts)
        send_telegram_alerts(messages, BOT_TOKEN, CHAT_ID)
        print(f"[알림] {len(messages)}건 전송 완료")
    # 상태 갱신
    initial = EconomicCalendarData(new_df)
    # 다음 타겟 시간 계산 및 타이머 재설정
    next_time = get_next_target_time(new_df)
    if next_time:
        print(f"[예약] 다음 타겟 발표시간: {next_time}")
        timer_until_window(next_time.to_pydatetime(), crawl_and_alert_and_reschedule)
    else:
        print("[종료] 더 이상 예정된 발표가 없습니다.")

if __name__ == "__main__":
    # 최초 타겟 시간 계산 및 타이머 시작
    first_df = get_calendar()
    next_time = get_next_target_time(first_df)
    if next_time:
        print(f"[시작] 첫 타겟 발표시간: {next_time}")
        timer_until_window(next_time.to_pydatetime(), crawl_and_alert_and_reschedule)
    else:
        print("[종료] 예정된 발표가 없습니다.")
    while True:
        time.sleep(60)  # 메인 스레드 유지
