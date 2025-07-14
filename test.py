import requests
import pandas as pd
from bs4 import BeautifulSoup

# TradingEconomics 캘린더 페이지 요청
url = "https://tradingeconomics.com/calendar"
headers = {
    "User-Agent": "Mozilla/5.0",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 경제지표 테이블 찾기
table = soup.find("table", {"id": "calendar"})
rows = table.find_all("tr", class_=lambda x: x != "calendar-header")  # 헤더 제외

data = []
tmp = []
for row in rows:
    cols = row.find_all("td")
    tmp.append(cols)
    #print(type(cols))
    #pd.DataFrame(cols).to_csv('check.csv')
    if len(cols) < 10:
        continue
    time = cols[0].text.strip()
    country = cols[1].img["title"].strip() if cols[1].find("img") else ""
    event = cols[2].text.strip()
    actual = cols[3].text.strip()
    forecast = cols[4].text.strip()
    previous = cols[5].text.strip()
    one = cols[6].text.strip()
    two = cols[7].text.strip()
    three = cols[8].text.strip()
    f = cols[9].text.strip()
    data.append({
        "시간": time,
        "국가": country,
        "지표명": event,
        "발표치": actual,
        "예상치": forecast,
        "이전치": previous,
        "one": one,
        "two": two,
        "three": three,
        "f": f
    })


tmp_df = pd.DataFrame(tmp)
tmp_df.to_csv('tmp.csv')
df_te_calendar = pd.DataFrame(data)
print(df_te_calendar)

df_te_calendar.to_csv('test.csv')