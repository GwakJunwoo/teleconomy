import emoji

def generate_emoji(country_name):
    # 국가명 -> ISO 2자리 코드 간단 매핑 (필요 시 확장 가능)
    name_to_code = {
        "United States": "US", "China": "CN", "Germany": "DE", "United Kingdom": "GB",
        "Japan": "JP", "France": "FR", "Canada": "CA", "Italy": "IT", "South Korea": "KR"
    }
    code = name_to_code.get(country_name, "")
    return country_to_emoji(code) if code else ""

def country_to_emoji(code):
    # ISO Alpha-2 코드 → 🇰🇷 이모지 형태
    OFFSET = 127397
    return ''.join([chr(ord(c) + OFFSET) for c in code.upper()])

def format_alert_messages(df):
    messages = []
    for _, row in df.iterrows():
        flag = generate_emoji(row['국가'])
        title = f"**{row['지표명']}** - {flag}"
        msg = [
            title,
            f"Country: {row['국가']} ({row['국가코드']})",
            f"Indicator: {row['지표명']}",
            f"Actual: {row['발표치_x']}",
            f"Forecast: {row['예측치_x']}",
            f"Previous: {row['이전치_x']}"
        ]
        messages.append('\n'.join(msg))
    return messages
