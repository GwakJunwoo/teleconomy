
from CalendarCrawler import get_calendar
from EconomicCalendar import EconomicCalendarData
from Timer import timer_until_window

from message import format_alert_messages
from telegram import send_telegram_alerts
import pandas as pd
import pytz
import os
import time

# 환경 변수 또는 직접 입력
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8083119806:AAHbMtmBORqBn_Co_JywKjcAqrsL1jNd46U')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1002424388234')


# 최초 데이터 적재 및 타겟 시간 계산
initial = EconomicCalendarData(get_calendar())

def get_next_target_time(df):
    now = pd.Timestamp.now() + pd.Timedelta(hours=9)  # UTC+9, tz-naive
    kst = pd.to_datetime(df['KST_DATETIME'], errors='coerce')  # tz-naive, KST 기준
    future = df[kst.notna() & (kst > now)]
    if not future.empty:
        return kst[future.index].min()
    return None


def crawl_and_alert_and_reschedule():
    global initial
    # 최신 데이터 크롤링
    new_df = get_calendar()
    print("[DEBUG] 크롤링된 데이터 상위 5개:")
    print(new_df.head())
    # 신규 알림 감지
    new_alerts = initial.compare_and_alert(new_df)
    print(f"[DEBUG] 신규 알림 감지 결과: {len(new_alerts)}건")
    if not new_alerts.empty:
        print("[DEBUG] 신규 알림 데이터:")
        print(new_alerts)
        # 메시지 생성 및 전송
        messages = format_alert_messages(new_alerts)
        send_telegram_alerts(messages, BOT_TOKEN, CHAT_ID)
        print(f"[알림] {len(messages)}건 전송 완료")
    # 상태 갱신
    initial = EconomicCalendarData(new_df)
    # 다음 타겟 시간 계산 및 타이머 재설정
    next_time = get_next_target_time(new_df)
    if next_time:
        now = pd.Timestamp.now() + pd.Timedelta(hours=9)
        wait_sec = (next_time - now).total_seconds()
        print(f"[예약] 다음 타겟 발표시간: {next_time} (현재시각: {now}, 대기 {int(wait_sec)}초)")
        print(f"[INFO] {next_time - pd.Timedelta(minutes=1)} ~ {next_time + pd.Timedelta(minutes=2)} 구간에서 30초 간격으로 크롤링/알림")
        timer_until_window(next_time.to_pydatetime(), crawl_and_alert_and_reschedule)
    else:
        print("[종료] 더 이상 예정된 발표가 없습니다.")

if __name__ == "__main__":
    # 최초 타겟 시간 계산 및 타이머 시작
    first_df = get_calendar()
    next_time = get_next_target_time(first_df)
    if next_time:
        now = pd.Timestamp.now() + pd.Timedelta(hours=9)
        wait_sec = (next_time - now).total_seconds()
        print(f"[시작] 첫 타겟 발표시간: {next_time} (현재시각: {now}, 대기 {int(wait_sec)}초)")
        print(f"[INFO] {next_time - pd.Timedelta(minutes=1)} ~ {next_time + pd.Timedelta(minutes=2)} 구간에서 30초 간격으로 크롤링/알림")
        timer_until_window(next_time.to_pydatetime(), crawl_and_alert_and_reschedule)
    else:
        print("[종료] 예정된 발표가 없습니다.")
    while True:
        time.sleep(60)  # 메인 스레드 유지
