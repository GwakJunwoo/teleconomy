import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def get_calendar():
    url = "https://tradingeconomics.com/calendar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # <tr> 요소들 찾기
    rows = soup.find_all("tr", attrs={"data-id": True})

    data = []

    for row in rows:
        try:
            # 날짜(class)에 포함된 시간 추출
            time_td = row.find("td", class_=lambda x: x and x.startswith("2025"))
            시간 = time_td.text.strip() if time_td else ""

            # 날짜(class 속성에서 추출)
            날짜 = None
            if time_td:
                for cls in time_td.get("class", []):
                    try:
                        날짜 = datetime.strptime(cls.strip(), "%Y-%m-%d").date()
                        break
                    except:
                        continue

            국가 = row.find("div", class_="flag")
            국가명 = 국가["title"].strip() if 국가 else ""

            국가코드 = row.find("td", class_="calendar-iso")
            국가코드 = 국가코드.text.strip() if 국가코드 else ""

            지표셀 = row.select_one("td:nth-of-type(3)")
            if 지표셀:
                a_tag = 지표셀.find("a", class_="calendar-event")
                if a_tag and a_tag.text.strip():
                    지표명 = a_tag.text.strip()
                else:
                    # <a>가 없으면 <span> 또는 td 자체 텍스트
                    텍스트후보 = [el for el in 지표셀.stripped_strings]
                    지표명 = 텍스트후보[0] if 텍스트후보 else ""
            else:
                지표명 = ""

            레퍼런스 = row.find("span", class_="calendar-reference")
            레퍼런스 = 레퍼런스.text.strip() if 레퍼런스 else ""

            발표치_tag = row.find("span", id="actual")
            발표치 = 발표치_tag.text.strip() if 발표치_tag else ""

            이전치_tag = row.find("span", id="previous")
            이전치 = 이전치_tag.text.strip() if 이전치_tag else ""

            예상치_tag = row.find("a", id="consensus")
            예상치 = 예상치_tag.text.strip() if 예상치_tag else ""

            예측치_tag = row.find("a", id="forecast")
            예측치 = 예측치_tag.text.strip() if 예측치_tag else ""

            # 한국 시간 기준 datetime 생성
            시간변환 = None
            if 시간 and 날짜:
                try:
                    dt = datetime.strptime(시간, "%I:%M %p")
                    시간변환 = datetime.combine(날짜, dt.time()) + timedelta(hours=9)
                except:
                    pass

            data.append({
                "시간": 시간,
                "KST_DATETIME": 시간변환,
                "국가": 국가명,
                "국가코드": 국가코드,
                "지표명": 지표명,
                "레퍼런스": 레퍼런스,
                "발표치": 발표치,
                "예상치": 예상치,
                "예측치": 예측치,
                "이전치": 이전치
            })
        except Exception:
            continue

    df_calendar_te = pd.DataFrame(data)
    return df_calendar_te


print(get_calendar())
get_calendar().to_csv("calendar_te.csv", index=False, encoding="utf-8-sig")