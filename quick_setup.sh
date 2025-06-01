#!/bin/bash

echo "🚀 텔레그램 포워더 봇 빠른 설정"
echo "================================"

# .env 파일 생성
if [ ! -f ".env" ]; then
    echo "📝 .env 파일을 생성합니다..."
    cp config.env.example .env
    echo "✅ .env 파일이 생성되었습니다."
else
    echo "✅ .env 파일이 이미 존재합니다."
fi

echo ""
echo "📋 다음 단계를 완료해주세요:"
echo ""
echo "1. 텔레그램 봇 생성:"
echo "   - @BotFather와 대화"
echo "   - /newbot 명령어로 봇 생성"
echo "   - 받은 토큰을 복사"
echo ""
echo "2. .env 파일 편집:"
echo "   nano .env"
echo "   또는"
echo "   open .env"
echo ""
echo "3. 필수 정보 입력:"
echo "   - BOT_TOKEN=받은_봇_토큰"
echo "   - GROUP_CHAT_ID=그룹_채팅_ID"
echo ""
echo "4. 봇 매핑 설정:"
echo "   python config_manager.py"
echo ""
echo "5. 봇 실행:"
echo "   python telegram_forwarder_bot.py"
echo ""
echo "📖 자세한 내용은 README.md를 참고하세요."
echo "🌐 24/7 운영 방법은 deploy_guide.md를 참고하세요." 