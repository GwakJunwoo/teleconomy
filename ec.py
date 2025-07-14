# 사용 예시:
# 기존 데이터와 새 데이터가 있다고 가정하고, 클래스 생성 및 비교
# ec = EconomicCalendarData(old_df)
# new_alerts = ec.compare_and_alert(new_df)

from CalendarCrawler import get_calendar
from EconomicCalendar import EconomicCalendarData
import pandas as pd
from message import *

ec = EconomicCalendarData(get_calendar())
new_alerts = ec.compare_and_alert(
    pd.read_csv('tt (4).csv', encoding='utf-8-sig', on_bad_lines='skip')
)

print(new_alerts)
new_alerts.to_csv('test.csv', encoding='utf-8-sig')

print(format_alert_messages(new_alerts))