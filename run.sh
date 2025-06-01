#!/bin/bash

# 텔레그램 포워더 봇 실행 스크립트

echo "=== 텔레그램 메시지 포워더 봇 ==="

# .env 파일 존재 확인
if [ ! -f ".env" ]; then
    echo "❌ .env 파일이 없습니다."
    echo "config.env.example 파일을 복사하여 .env 파일을 생성하고 설정을 완료해주세요."
    echo ""
    echo "cp config.env.example .env"
    echo "nano .env  # 또는 다른 에디터로 편집"
    exit 1
fi

# Python 가상환경 확인 (선택사항)
if [ -d "venv" ]; then
    echo "🔄 가상환경 활성화 중..."
    source venv/bin/activate
fi

# 의존성 설치 확인
echo "📦 의존성 확인 중..."
pip install -r requirements.txt > /dev/null 2>&1

# 봇 실행
echo "🚀 봇을 시작합니다..."
echo "중단하려면 Ctrl+C를 누르세요."
echo ""

python telegram_forwarder_bot.py 