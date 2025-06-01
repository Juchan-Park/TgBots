# 24/7 서버 배포 가이드

컴퓨터가 꺼져도 텔레그램 봇이 계속 작동하도록 하는 방법들을 안내합니다.

## 옵션 1: 무료 클라우드 서비스 (추천)

### Railway (무료 플랜 제공)

1. **Railway 계정 생성**
   - [Railway.app](https://railway.app) 방문
   - GitHub 계정으로 로그인

2. **프로젝트 배포**
   ```bash
   # Railway CLI 설치 (선택사항)
   npm install -g @railway/cli
   
   # 또는 웹 인터페이스에서 GitHub 저장소 연결
   ```

3. **환경 변수 설정**
   - Railway 대시보드에서 환경 변수 추가:
     - `BOT_TOKEN`: 텔레그램 봇 토큰
     - `GROUP_CHAT_ID`: 그룹 채팅 ID

### Render (무료 플랜 제공)

1. **Render 계정 생성**
   - [Render.com](https://render.com) 방문
   - GitHub 계정으로 로그인

2. **Web Service 생성**
   - "New Web Service" 선택
   - GitHub 저장소 연결
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python telegram_forwarder_bot.py`

### Heroku (유료 전환됨)

1. **Heroku 계정 생성**
   - [Heroku.com](https://heroku.com) 방문

2. **Heroku CLI 설치 및 배포**
   ```bash
   # Heroku CLI 설치 (macOS)
   brew tap heroku/brew && brew install heroku
   
   # 로그인
   heroku login
   
   # 앱 생성
   heroku create your-bot-name
   
   # 환경 변수 설정
   heroku config:set BOT_TOKEN=your_bot_token
   heroku config:set GROUP_CHAT_ID=your_group_id
   
   # 배포
   git push heroku main
   ```

## 옵션 2: VPS (Virtual Private Server)

### DigitalOcean, Linode, Vultr 등

1. **VPS 구매** (월 $5~10)
2. **Ubuntu 서버 설정**
3. **봇 배포 및 실행**

## 옵션 3: 라즈베리 파이

집에서 24/7 운영할 수 있는 저전력 솔루션

## 배포용 파일 준비

### Procfile (Heroku/Railway용)

```
worker: python telegram_forwarder_bot.py
```

### Dockerfile (컨테이너 배포용)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "telegram_forwarder_bot.py"]
```

### runtime.txt (일부 플랫폼용)

```
python-3.9.18
```

## 환경 변수 설정 방법

각 플랫폼에서 다음 환경 변수를 설정해야 합니다:

- `BOT_TOKEN`: 텔레그램 봇 토큰
- `GROUP_CHAT_ID`: 그룹 채팅 ID
- (선택사항) `TARGET_TOPIC_ID`, `SOURCE_BOT_USERNAME`: 레거시 설정

## 추천 순서

1. **Railway** - 가장 쉽고 무료
2. **Render** - 안정적이고 무료
3. **VPS** - 더 많은 제어권이 필요한 경우
4. **라즈베리 파이** - 집에서 운영하고 싶은 경우

## 주의사항

- 무료 플랜은 사용량 제한이 있을 수 있습니다
- 중요한 봇의 경우 유료 플랜 고려
- 환경 변수에 민감한 정보 저장 시 보안 주의 