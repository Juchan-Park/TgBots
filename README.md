# 텔레그램 메시지 포워더 봇

여러 봇이 메인 채널에 보내는 메시지를 각각 다른 토픽으로 자동 포워딩하는 텔레그램 봇입니다.

## 🚀 빠른 시작 (Railway 배포)

### 1. GitHub에 업로드
```bash
# 이미 Git이 초기화되어 있습니다
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

### 2. Railway 배포
1. [Railway.app](https://railway.app)에서 GitHub 로그인
2. "Deploy from GitHub repo" 선택
3. 이 저장소 선택
4. 환경 변수 설정:
   - `BOT_TOKEN`: 텔레그램 봇 토큰
   - `GROUP_CHAT_ID`: 그룹 채팅 ID

**📖 자세한 Railway 배포 가이드**: [railway_deploy_guide.md](railway_deploy_guide.md)

## 기능

- **다중 봇 매핑**: 여러 봇의 메시지를 각각 다른 토픽으로 포워딩
- **유연한 설정**: JSON 파일을 통한 쉬운 봇-토픽 매핑 관리
- **설정 관리 도구**: 대화형 인터페이스로 매핑 설정 관리
- **하위 호환성**: 기존 단일 봇 설정도 지원
- **모든 메시지 타입 지원**: 텍스트, 이미지, 문서, 비디오, 음성, 스티커 등
- **실시간 로깅**: 동작 상태 확인 가능

## 설치 및 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 텔레그램 봇 생성

1. 텔레그램에서 [@BotFather](https://t.me/BotFather)와 대화 시작
2. `/newbot` 명령어로 새 봇 생성
3. 봇 이름과 사용자명 설정
4. 받은 토큰을 복사해두기

### 3. 환경 변수 설정

`config.env.example` 파일을 복사하여 `.env` 파일을 생성:

```bash
cp config.env.example .env
```

`.env` 파일에서 필수 정보 입력:
```
BOT_TOKEN=your_bot_token_here
GROUP_CHAT_ID=your_group_chat_id_here
```

### 4. 봇 매핑 설정

#### 방법 1: 설정 관리 도구 사용 (권장)

```bash
python config_manager.py
```

대화형 인터페이스를 통해 봇 매핑을 쉽게 관리할 수 있습니다:
- 봇 매핑 추가/수정/삭제
- 설정 보기/수정
- 실시간 설정 저장

#### 방법 2: JSON 파일 직접 편집

`bot_mapping.json` 파일을 직접 편집:

```json
{
  "bot_mappings": [
    {
      "source_bot_username": "news_bot",
      "target_topic_id": 123,
      "description": "뉴스 봇의 메시지를 뉴스 토픽으로"
    },
    {
      "source_bot_username": "weather_bot",
      "target_topic_id": 456,
      "description": "날씨 봇의 메시지를 날씨 토픽으로"
    }
  ],
  "settings": {
    "forward_all_unknown_bots": false,
    "default_topic_id": null,
    "log_unknown_bots": true
  }
}
```

### 5. 필요한 정보 확인

#### 5.1 그룹 채팅 ID와 토픽 ID 확인

1. 생성한 봇을 그룹에 추가
2. 그룹에서 메시지를 보내기
3. 설정 도우미 스크립트 실행:

```bash
python setup_helper.py
```

## 사용법

### 봇 실행

```bash
python telegram_forwarder_bot.py
```

또는 실행 스크립트 사용:

```bash
./run.sh
```

### 동작 방식

1. 봇이 그룹의 모든 메시지를 모니터링
2. 메인 채널(토픽이 없는 곳)에서 매핑된 봇의 메시지를 감지
3. 각 봇의 메시지를 해당하는 토픽으로 자동 포워딩

## 설정 옵션

### 봇 매핑 설정

- `source_bot_username`: 감지할 봇의 사용자명
- `target_topic_id`: 메시지를 포워딩할 토픽 ID
- `description`: 매핑에 대한 설명 (선택사항)

### 일반 설정

- `forward_all_unknown_bots`: 매핑되지 않은 봇도 포워딩할지 여부
- `default_topic_id`: 알 수 없는 봇을 위한 기본 토픽 ID
- `log_unknown_bots`: 매핑되지 않은 봇 메시지를 로그에 기록할지 여부

## 설정 예시

### 다중 봇 매핑 예시

```json
{
  "bot_mappings": [
    {
      "source_bot_username": "crypto_alerts_bot",
      "target_topic_id": 100,
      "description": "암호화폐 알림 봇"
    },
    {
      "source_bot_username": "stock_news_bot",
      "target_topic_id": 200,
      "description": "주식 뉴스 봇"
    },
    {
      "source_bot_username": "weather_updates",
      "target_topic_id": 300,
      "description": "날씨 업데이트 봇"
    }
  ],
  "settings": {
    "forward_all_unknown_bots": false,
    "default_topic_id": null,
    "log_unknown_bots": true
  }
}
```

### 환경 변수 예시

```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GROUP_CHAT_ID=-1001234567890
```

## 배포 옵션

### 🌟 Railway (추천 - 무료)
- **가이드**: [railway_deploy_guide.md](railway_deploy_guide.md)
- **장점**: 쉬운 설정, GitHub 연동, 무료 플랜
- **제한**: 월 500시간 실행 시간

### 기타 옵션
- **상세 가이드**: [deploy_guide.md](deploy_guide.md)
- Render, Heroku, VPS, 라즈베리 파이 등

## 주의사항

1. **봇 권한**: 봇이 그룹에서 메시지를 읽고 보낼 수 있는 권한이 있어야 합니다.
2. **토픽 기능**: 그룹에서 토픽 기능이 활성화되어 있어야 합니다.
3. **관리자 권한**: 봇을 그룹 관리자로 설정하는 것을 권장합니다.
4. **토픽 ID**: 각 토픽의 정확한 ID를 확인해야 합니다.
5. **보안**: `.env` 파일은 GitHub에 업로드하지 마세요 (`.gitignore`에 포함됨).

## 문제 해결

### 봇이 메시지를 감지하지 못하는 경우

1. 봇이 그룹에 올바르게 추가되었는지 확인
2. `bot_mapping.json`의 봇 사용자명이 정확한지 확인
3. 기존 봇이 메인 채널(토픽이 아닌 곳)에 메시지를 보내는지 확인

### 토픽으로 메시지가 전송되지 않는 경우

1. 토픽 ID가 올바른지 확인
2. 봇이 해당 토픽에 메시지를 보낼 권한이 있는지 확인
3. 토픽이 실제로 존재하는지 확인

### 설정 관리

```bash
# 설정 관리 도구 실행
python config_manager.py

# 현재 설정 확인
python setup_helper.py
```

### 로그 확인

봇 실행 시 콘솔에 출력되는 로그를 통해 동작 상태를 확인할 수 있습니다:

```
2024-01-01 12:00:00 - __main__ - INFO - 텔레그램 포워더 봇을 시작합니다...
2024-01-01 12:00:00 - __main__ - INFO - 봇 매핑 로드 완료: 3개 봇 설정
2024-01-01 12:00:00 - __main__ - INFO -   @news_bot -> 토픽 123 (뉴스 봇)
2024-01-01 12:00:01 - __main__ - INFO - 봇 메시지 감지: @news_bot -> 토픽 123
2024-01-01 12:00:01 - __main__ - INFO - 메시지를 토픽 123로 포워딩 완료
```

## 하위 호환성

기존 단일 봇 설정도 계속 지원됩니다. `bot_mapping.json` 파일이 없으면 환경 변수의 `TARGET_TOPIC_ID`와 `SOURCE_BOT_USERNAME` 설정을 사용합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 