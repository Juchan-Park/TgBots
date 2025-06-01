# Railway 배포 가이드

Railway를 사용하여 텔레그램 봇을 24/7 운영하는 방법을 안내합니다.

## 1. GitHub 저장소 준비

### 1.1 Git 초기화 및 커밋

```bash
# Git 저장소 초기화 (아직 안 했다면)
git init

# 모든 파일 추가 (.gitignore가 민감한 정보 제외)
git add .

# 첫 커밋
git commit -m "Initial commit: Telegram forwarder bot"

# GitHub에 저장소 생성 후 연결
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

### 1.2 .env 파일 확인

`.env` 파일이 `.gitignore`에 포함되어 GitHub에 업로드되지 않는지 확인:

```bash
# .env 파일이 Git에서 추적되지 않는지 확인
git status
```

`.env` 파일이 목록에 나타나지 않아야 합니다.

## 2. Railway 배포

### 2.1 Railway 계정 생성

1. [Railway.app](https://railway.app) 방문
2. "Login with GitHub" 클릭
3. GitHub 계정으로 로그인

### 2.2 새 프로젝트 생성

1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. 방금 생성한 저장소 선택
4. "Deploy Now" 클릭

### 2.3 환경 변수 설정

1. 배포된 프로젝트 클릭
2. "Variables" 탭 클릭
3. 다음 환경 변수들을 추가:

```
BOT_TOKEN=your_actual_bot_token_here
GROUP_CHAT_ID=your_actual_group_chat_id_here
```

**중요**: 실제 값으로 교체해야 합니다!

### 2.4 서비스 타입 설정

1. "Settings" 탭으로 이동
2. "Service" 섹션에서 확인:
   - Start Command: `python telegram_forwarder_bot.py`
   - 또는 Procfile이 자동으로 감지됨

## 3. 봇 토큰 및 그룹 ID 확인

### 3.1 봇 토큰 얻기

1. 텔레그램에서 [@BotFather](https://t.me/BotFather)와 대화
2. `/newbot` 명령어 입력
3. 봇 이름과 사용자명 설정
4. 받은 토큰을 복사 (예: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3.2 그룹 채팅 ID 확인

방법 1: 봇을 그룹에 추가 후 확인
```bash
# 로컬에서 setup_helper.py 실행
python setup_helper.py
```

방법 2: 웹 API 사용
1. 봇을 그룹에 추가
2. 그룹에서 메시지 전송
3. 브라우저에서 접속: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
4. 응답에서 `chat.id` 값 확인 (음수 값)

## 4. 봇 매핑 설정

### 4.1 로컬에서 설정 후 업로드

```bash
# 봇 매핑 설정
python config_manager.py

# 변경사항 커밋 및 푸시
git add bot_mapping.json
git commit -m "Update bot mappings"
git push
```

### 4.2 Railway에서 자동 재배포

Git push 후 Railway가 자동으로 재배포합니다.

## 5. 배포 확인

### 5.1 로그 확인

1. Railway 대시보드에서 프로젝트 클릭
2. "Deployments" 탭에서 최신 배포 클릭
3. "View Logs" 클릭
4. 다음과 같은 로그가 나타나야 함:

```
텔레그램 포워더 봇을 시작합니다...
그룹 ID: -1001234567890
봇 매핑 로드 완료: 2개 봇 설정
```

### 5.2 봇 테스트

1. 텔레그램 그룹에서 매핑된 봇이 메시지 전송
2. 해당 토픽에 메시지가 포워딩되는지 확인

## 6. 문제 해결

### 6.1 배포 실패

**오류**: `ModuleNotFoundError`
- **해결**: `requirements.txt` 파일 확인

**오류**: `ValueError: 필수 환경 변수가 설정되지 않았습니다`
- **해결**: Railway Variables에서 환경 변수 확인

### 6.2 봇이 응답하지 않음

1. Railway 로그에서 오류 확인
2. 봇 토큰이 올바른지 확인
3. 그룹 ID가 올바른지 확인
4. 봇이 그룹에 추가되어 있는지 확인

### 6.3 메시지가 포워딩되지 않음

1. `bot_mapping.json` 설정 확인
2. 봇 사용자명이 정확한지 확인
3. 토픽 ID가 올바른지 확인

## 7. 업데이트 방법

코드 변경 후:

```bash
git add .
git commit -m "Update bot functionality"
git push
```

Railway가 자동으로 재배포합니다.

## 8. 비용 및 제한사항

### Railway 무료 플랜:
- 월 500시간 실행 시간
- 1GB RAM
- 1GB 디스크
- 소규모 봇에 충분함

### 유료 플랜 ($5/월):
- 무제한 실행 시간
- 더 많은 리소스

## 9. 보안 팁

1. ✅ `.env` 파일을 `.gitignore`에 포함
2. ✅ 환경 변수는 Railway Variables에서만 설정
3. ✅ 봇 토큰을 코드에 하드코딩하지 않기
4. ✅ 정기적으로 봇 토큰 재생성 고려

이제 Railway에서 24/7 봇 운영이 가능합니다! 🚀 