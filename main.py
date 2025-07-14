
from CalendarCrawler import get_calendar
from EconomicCalendar import EconomicCalendarData
from Timer import timer_until_window

from message import format_alert_messages
from telegram import send_telegram_alerts
import pandas as pd
import pytz
import os
import time


# ================= 환경설정 =================
def get_env():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '8083119806:AAHbMtmBORqBn_Co_JywKjcAqrsL1jNd46U')
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '-1002424388234')
    return bot_token, chat_id


# ================= 타겟 시간 계산 =================
def get_next_target_time(df):
    now = pd.Timestamp.now(tz='Asia/Seoul')
    kst = pd.to_datetime(df['KST_DATETIME'], errors='coerce').dt.tz_localize('Asia/Seoul', nonexistent='NaT', ambiguous='NaT')
    future = df[kst.notna() & (kst > now)]
    if not future.empty:
        return kst[future.index].min()
    return None


# ================= 알림 시스템 클래스 =================
class AlertSystem:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.initial = EconomicCalendarData(get_calendar())
        self._last_scheduled = None  # 중복 예약 차단용

    def crawl_and_alert_and_reschedule(self):
        print("\n[DEBUG] === crawl_and_alert_and_reschedule() 진입 ===")
        new_df = get_calendar()
        print("[DEBUG] 크롤링된 데이터 가장 최근값:")
        print(new_df.tail(1))

        new_alerts = self.initial.compare_and_alert(new_df)
        if not new_alerts.empty:
            messages = format_alert_messages(new_alerts)
            send_telegram_alerts(messages, self.bot_token, self.chat_id)
            print(f"[알림] {len(messages)}건 전송 완료")

        self.initial = EconomicCalendarData(new_df)

        # --- 중복 예약 차단 로직 ---
        next_time = get_next_target_time(new_df)
        if next_time:
            if self._last_scheduled and next_time == self._last_scheduled:
                print(f"[중복예약 차단] 이미 {next_time} 예약됨 → skip")
                return
            self._last_scheduled = next_time

            now = pd.Timestamp.now(tz='Asia/Seoul')
            print(f"[예약] 다음 타겟 발표시간: {next_time}")
            timer_until_window(next_time.to_pydatetime(), self.crawl_and_alert_and_reschedule)
        else:
            print("[종료] 더 이상 예정된 발표가 없습니다.")


# ================= 진입점 =================
def main():
    print("[DEBUG] main() 진입")
    bot_token, chat_id = get_env()
    alert_system = AlertSystem(bot_token, chat_id)

    first_df = get_calendar()
    print("[DEBUG] 최초 get_calendar() 결과 상위 3개:")
    print(first_df.head(3))

    next_time = get_next_target_time(first_df)
    if next_time:
        now = pd.Timestamp.now(tz='Asia/Seoul')
        wait_sec = (next_time - now).total_seconds()
        print(f"[시작] 첫 타겟 발표시간: {next_time} (현재시각: {now}, 대기 {int(wait_sec)}초)")
        print(f"[INFO] {next_time - pd.Timedelta(minutes=1)} ~ {next_time + pd.Timedelta(minutes=2)} 구간에서 30초 간격으로 크롤링/알림")
        print("[DEBUG] timer_until_window 호출")
        timer_until_window(next_time.to_pydatetime(), alert_system.crawl_and_alert_and_reschedule)
    else:
        print("[종료] 예정된 발표가 없습니다.")

    # 메인 스레드 유지
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()