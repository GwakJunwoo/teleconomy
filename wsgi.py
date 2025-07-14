import sys
import os

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(__file__))

from main import main

def application(environ, start_response):
    status = '200 OK'
    output = b'Hello from teleconomy!'
    start_response([(b'Content-type', b'text/plain')], status)
    # 실제 서비스용 엔드포인트는 별도 구현 필요
    return [output]
