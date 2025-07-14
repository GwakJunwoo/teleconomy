import requests
import os

def send_telegram_alerts(messages: list[str], bot_token: str, chat_id: str) -> None:
    """
    텔레그램 봇을 통해 메시지 리스트를 차례대로 전송
    메시지는 MarkdownV2 포맷에 맞게 escape됨
    """
    def escape_markdown(text: str) -> str:
        escape_chars = r"_\*\[\]\(\)~`>#+\-=|{}.!"
        return ''.join(['\\' + c if c in escape_chars else c for c in text])

    for msg in messages:
        escaped_msg = escape_markdown(msg)
        payload = {
            "chat_id": chat_id,
            "text": escaped_msg,
            "parse_mode": "MarkdownV2"
        }
        response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data=payload)
        if response.status_code != 200:
            print(f"[❌] 전송 실패: {response.status_code}, {response.text}")
        else:
            print("[✅] 전송 완료")