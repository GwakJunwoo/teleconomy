import pandas as pd
from datetime import datetime, timedelta

def get_calendar():
    # 현재 시각 기준 -5 ~ +10분 구간의 1분 간격 데이터 생성
    now = datetime.now() + timedelta(hours=9)
    base_time = now.replace(second=0, microsecond=0)
    data = []
    for i in range(-5, 11):  # -5분 ~ +10분
        kst_dt = base_time + timedelta(minutes=i)
        # 발표치는 해당 시간(KST_DATETIME)이 현재시각 이하일 때만 채워짐
        actual = f"{2.0 + i}%" if kst_dt <= now else ""
        data.append({
            "시간": kst_dt.strftime("%I:%M %p"),
            "KST_DATETIME": kst_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "국가": "Japan",
            "국가코드": "JP",
            "지표명": f"MOCK_INDICATOR_{i+6}",
            "레퍼런스": "MOCK",
            "발표치": actual,
            "예상치": "2.0%",
            "예측치": "2.1%",
            "이전치": "1.9%"
        })
    return pd.DataFrame(data)
