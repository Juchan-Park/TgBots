FROM python:3.9-slim

WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 봇 실행
CMD ["python", "telegram_forwarder_bot.py"] 